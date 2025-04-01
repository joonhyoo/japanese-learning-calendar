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

task_options = "\n".join(
    f"\t{key}: {value}" for key, value in task_mapping.items())

completed_task_msg = (
    'What did you complete?\n'
    'You can write more than one by separating with a space)\n'
    f'{task_options}\n'
)


def main():
    study_date = datetime.today()
    completed_tasks = []
    day = input('Today or (Y)esterday? ')
    if (day.lower() == 'y'):
        study_date = study_date - timedelta(days=1)
    study_date = study_date.strftime('%Y-%m-%d')

    tasks = input(completed_task_msg).split(' ')
    tasks_to_process = [task for task in tasks if task in task_mapping]
    for task in tasks_to_process:
        print(task_mapping[task])
        if task == 'a':
            # ToDo: think about how to in sql
            print('not implemented yet')
        elif task == 'x':
            clear_study_records(study_date)
        else:
            completed_tasks.append(task)
    len(completed_tasks) > 0 and pushChanges(study_date, completed_tasks)
    print_completed_tasks(study_date)


def clear_study_records(study_date):
    response = (
        supabase.table("studied_items")
        .delete()
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .execute()
    )
    print('deleting items studied on', study_date)
    print(len(response.data), 'item/s deleted')


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


def getStudyRow(study_date, item):
    check_response = (
        supabase.table("studied_items")
        .select("count")
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .eq("material_id", item)
        .execute()
    )
    return check_response.data


def updateStudyRow(study_date, new_count, item):
    update_response = (
        supabase.table("studied_items")
        .update({'count': new_count})
        .eq("study_date", study_date)
        .eq("user_id", uid)
        .eq("material_id", item)
        .execute()
    )
    print('updated row:', update_response.data)


def insertStudyRow(study_date, item):
    insert_response = (
        supabase.table("studied_items")
        .insert({'user_id': uid, 'study_date': study_date, 'material_id': item})
        .execute()
    )
    print('inserted new row:', insert_response.data)


def pushChanges(study_date, completed_tasks):
    if doesRecordExist(study_date):
        print('user with that record exists, skipping')
    else:
        insertStudyRecord(study_date)
    for item in completed_tasks:
        if item is None:
            continue
        rowData = getStudyRow(study_date, item)
        if (rowData):
            print('row already exists, updating count to: ',
                  rowData[0]['count'])
            new_count = int(rowData[0]['count']) + 1
            updateStudyRow(study_date, new_count, item)
        else:
            insertStudyRow(study_date, item)


main()
