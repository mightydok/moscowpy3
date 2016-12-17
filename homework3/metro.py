# encoding: utf-8

import json
import sys
from datetime import datetime

try:
    with open('data_metro_20161217.json', 'r', encoding='cp1251') as f:
        # Загружаем json, на выходе список
        metrodata = json.load(f)
        # Получаем сегодняшнее число и время
        dt_now = datetime.now()
        # Список станций где идет ремонт
        uniq = []
        # Внутри каждого элемента списка словарь
        for line in metrodata:
            # Если ключь в словаре заполнен
            if len(line['RepairOfEscalators']) > 0:
                # Получаем даты проведения ремонта, начало и окончание
                repairdates = line['RepairOfEscalators'][0]['RepairOfEscalators'].split('-')
                repair_start_day = datetime.strptime(repairdates[0], '%d.%m.%Y')
                repair_end_day = datetime.strptime(repairdates[1], '%d.%m.%Y')
                # Наполняем список станций где идет ремонт
                if repair_start_day <= dt_now <= repair_end_day:
                    if line['NameOfStation'] not in uniq:
                        uniq.append(line['NameOfStation'])

        print('Список станций где идет хотя бы один ремонт: {}'.format(', '.join(uniq)))

except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
