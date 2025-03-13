import json
from datetime import datetime, date, timedelta

# Dev tool atm for me to update the json data
# This will be replaced by the front end once I implement backend w db
# and user auth

# use dictionary instead to reduce repetitiveness
task_mapping = {
    'c': 'check studied',
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


with open('./src/data.json') as jsonData:
    data = json.load(jsonData)


def main():
    # load_dates()
    target_day = datetime.today()
    day = input('Today or (Y)esterday? ')

    if (day.lower() == 'y'):
        target_day = target_day - timedelta(days=1)
    target_day = target_day.strftime('%Y-%m-%d')

    tasks = input(completed_task_msg).split(' ')

    for task in tasks:
        handle_completed_task(task, target_day)

    print_points(target_day)

    with open('./src/data.json', 'w') as jsonData:
        json.dump(data, jsonData)


def handle_completed_task(task, target_day):
    if task in task_mapping:
        print(task_mapping[task])

        if task == 'a':  # Additional study requires extra input
            material = input('What did you study? ')
            study_time = input('How long did you study? ')
            add_points(material, target_day, study_time)
        elif task == 'x':
            reset_points(target_day)
        elif task == 'c':
            pass    # material gets printed from main, this is just a bypass
        else:
            add_points(task, target_day)
    else:
        print('Invalid input')


def add_date(given_date):
    data.append({'date': given_date, 'studied': [], 'additional': {}})


def load_dates():
    # tool to quickly load all dates into calendar
    sdate = date(2025, 1, 1)
    edate = date(2025, 12, 31)
    currdate = sdate

    while currdate <= edate:
        curr_date_str = currdate.strftime('%Y-%m-%d')
        if not date_exists(curr_date_str):
            add_date(curr_date_str)
        currdate += timedelta(days=1)

    data.sort(key=lambda r: r['date'])


def date_exists(given_date):
    for item in data:
        if item['date'] == given_date:
            return True

    return False


def add_points(material, target_day, hours=None):
    for x in data:
        if (x['date'] == target_day):
            if (hours):
                print(material, hours)
                x['additional'][material] = hours
            else:
                x['studied'].append(material)


def reset_points(given_date):
    for x in data:
        if (x['date'] == given_date):
            x['studied'] = []
            x['additional'] = {}


def print_points(given_date):
    for x in data:
        if (x['date'] == given_date):
            print(f"Studied on {x['date']}:", x['studied'])
            print('Additional study:', x['additional'])


main()
