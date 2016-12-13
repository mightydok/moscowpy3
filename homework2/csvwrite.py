# encoding: utf-8

import csv

answer_list = [
    { 'key': 'ты кто?', 'value': 'Дед Пихто!' },
    { 'key': 'что делаешь?', 'value': 'Сижу в чатике, курю кальян' },
    { 'key': 'норм', 'value': 'Ну и отлично, у меня то же все норм' }
]

with open('export.csv', 'w', encoding='utf-8') as f:
    fields = ['key', 'value']
    writer = csv.DictWriter(f, fields, delimiter=';')
    writer.writeheader()
    for answer in answer_list:
        writer.writerow(answer)
