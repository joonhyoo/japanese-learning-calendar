import json
from datetime import datetime, date, timedelta

today = datetime.today().strftime('%Y-%m-%d')\

completed_task_msg = """What did you do today?
(you can write more than one by adding a space)
    b: bunpro daily lessons
    w: wanikani daily lessons
    r: review session
    a: additional study
    x: reset score
"""


with open('./src/data.json') as jsonData:
    data = json.load(jsonData)


def main():
    # load_dates()
    tasks = input(completed_task_msg).split(' ')

    for task in tasks:
        handle_completed_task(task)

    with open('./src/data.json', 'w') as jsonData:
        json.dump(data, jsonData)


def handle_completed_task(task):
    if not date_exists(today):
        add_date(today)
    match task:
        case 'b':
            print('bunpro daily lessons')
            add_points(task)
        case 'w':
            print('wanikani daily lessons')
            add_points(task)
        case 'r':
            print('review')
            add_points(task)
        case 'a':
            print('additional study')
            material = input('what did you study? ')
            study_time = input('how long did you study? ')
            add_points(material, study_time)
        case 'x':
            print('reset score')
            reset_points(today)
        case _:
            print('invalid input')


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


def add_points(material, hours=None):
    for x in data:
        if (x['date'] == today):
            if (hours):
                print(material, hours)
                x['additional'][material] = hours
            else:
                x['studied'].append(material)


def reset_points(given_date):
    for x in data:
        if (x['date'] == given_date):
            x = {'date': given_date, 'studied': [], 'additional': {}}


main()
