import json
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')\

completed_task_msg = """What did you do today?
(you can write more than one by adding a space)
    l: lessons
    r: review session
    a: additional study
    x: reset score
"""

with open('./src/data.json') as jsonData:
    data = json.load(jsonData)


def main():
    tasks = input(completed_task_msg).split(' ')

    for task in tasks:
        handle_completed_task(task)

    with open('./src/data.json', 'w') as jsonData:
        json.dump(data, jsonData)


def handle_completed_task(task):
    if not date_exists():
        data.append({'date': today, 'count': 0})
    match task:
        case 'l':
            print('lesson')
            add_points(2)
        case 'r':
            print('review')
            add_points(1)
        case 'a':
            print('additional study')
            study_time = input('how many hours of study? ')
            add_points(int(study_time))
        case 'x':
            print('reset score')
            reset_points()
        case _:
            print('invalid input')


def date_exists():
    for item in data:
        if item['date'] == today:
            return True

    return False


def add_points(num):
    for x in data:
        if (x['date'] == today):
            x['count'] += num


def reset_points():
    for x in data:
        if (x['date'] == today):
            x['count'] = 0


main()
