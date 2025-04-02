import os
from dotenv import load_dotenv
from datetime import datetime, date, timedelta
from supabase import create_client, Client


load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
uid = os.getenv("PERSONAL_UID")
supabase: Client = create_client(url, key)

# I'm going to update a single array, and then push those changes into the
# records instead of modifying and reading the entire json file


# use dictionary instead to reduce repetitiveness
task_mapping = {
    'b': 'bunpro daily lessons',
    'w': 'wanikani daily lessons',
    'r': 'review session',
    'a': 'additional study',
    'x': 'reset score'
}

id_mapping = {
    'w': 1,
    'b': 2,
    'r': 3,
}

task_options = "\n".join(
    f"\t{key}: {value}" for key, value in task_mapping.items())

completed_task_msg = (
    'What did you complete?\n'
    'You can write more than one by separating with a space)\n'
    f'{task_options}\n'
)


def main():
    completed_tasks = []
    study_date = datetime.today().strftime("%Y-%m-%d")
    day = input('Today or insert date YYYY-MM-DD\t')
    if (len(day)):
        study_date = datetime.strptime(day, "%Y-%m-%d")
    print('study date is:', study_date)
    tasks = input(completed_task_msg).split(' ')
    tasks_to_process = [task for task in tasks if task in task_mapping]
    for task in tasks_to_process:
        print(task_mapping[task])
        if task == 'a':
            handle_additional_study(study_date)
        elif task == 'x':
            clear_study_records(study_date)
        else:
            material_id = id_mapping[task]
            completed_tasks.append(material_id)
    len(completed_tasks) > 0 and pushChanges(study_date, completed_tasks)
    print_completed_tasks(study_date)


def handle_additional_study(study_date):
    material_title = input('What did you study? ').lower()
    study_time = input('How long did you study? ')
    material_data = get_additional_study(material_title)
    if (not material_data):
        material_id = add_material(material_title)
    else:
        material_id = material_data[0]['id']
    insertStudiedItem(study_date, material_id)
    updateStudiedItem(study_date, study_time, material_id)


def add_material(material_title):
    insert_response = (
        supabase.table("study_material")
        .insert({'user_id': uid, 'title': material_title})
        .execute()
    )
    print('inserted new material', f"'{material_title}'", insert_response.data)
    return insert_response.data[0]['id']


def get_additional_study(material_title):
    check_response = (
        supabase.table("study_material")
        .select('*')
        .eq("title", material_title)
        .eq("user_id", uid)
        .execute()
    )
    return check_response.data


def clear_study_records(study_date):
    response = (
        supabase.table("studied_items")
        .delete()
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .execute()
    )
    if (not len(response.data)):
        print('there was nothing to delete.')
    else:
        print('deleting items studied on', study_date)
        total_count = sum(item["count"] for item in response.data)
        print(total_count, 'points deleted')


def print_completed_tasks(study_date):
    response = (
        supabase.table("study_records")
        .select("user_profile(user_name), study_material(title), studied_items(count)")
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .execute()
    )
    if (response.data):
        data = response.data[0]
        study_material = data['study_material']
        count = data['studied_items']
        user_name = data['user_profile']['user_name']
        print(user_name, 'studied on', study_date)
        for x, y in zip(study_material, count):
            print(x['title'], 'x', y['count'])
    else:
        print('nothing studied on', study_date)


def doesRecordExist(study_date):
    response = (
        supabase.table("study_records")
        .select("*")
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .execute()
    )
    return bool(response.data)


def insertStudyRecord(study_date):
    insert_response = (
        supabase.table("study_records")
        .insert({'study_date': study_date, 'user_id': uid})
        .execute()
    )
    print("Inserted new record:", insert_response.data)


def getStudyRow(study_date, material_id):
    check_response = (
        supabase.table("studied_items")
        .select("count")
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .eq("material_id", material_id)
        .execute()
    )
    return check_response.data


def updateStudiedItem(study_date, new_count, material_id):
    update_response = (
        supabase.table("studied_items")
        .update({'count': new_count})
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .eq("material_id", material_id)
        .execute()
    )
    print('updated row:', update_response.data)


def insertStudiedItem(study_date, material_id):
    insert_response = (
        supabase.table("studied_items")
        .insert({'user_id': uid, 'study_date': study_date, 'material_id': material_id})
        .execute()
    )
    print('inserted new row:', insert_response.data)


def pushChanges(study_date, completed_tasks):
    if doesRecordExist(study_date):
        print('user with that record exists, skipping')
    else:
        insertStudyRecord(study_date)
    for material_id in completed_tasks:
        if material_id is None:
            continue
        rowData = getStudyRow(study_date, material_id)
        if (rowData):
            new_count = int(rowData[0]['count']) + 1
            print('row already exists, updating count to: ',
                  new_count)
            updateStudiedItem(study_date, new_count, material_id)
        else:
            insertStudiedItem(study_date, material_id)


main()
