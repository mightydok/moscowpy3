# encoding: utf-8

import csv
import sys

answer_list = [
    { 'key': 'ты кто?', 'value': 'Дед Пихто!' },
    { 'key': 'что делаешь?', 'value': 'Сижу в чатике, курю кальян' },
    { 'key': 'норм', 'value': 'Ну и отлично, у меня то же все норм' }
]

try:
    with open('export.csv', 'w', encoding='utf-8') as f:
        fields = ['key', 'value']
        writer = csv.DictWriter(f, fields, delimiter=';')
        writer.writeheader()
        for answer in answer_list:
            writer.writerow(answer)
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
