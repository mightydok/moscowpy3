# encoding: utf-8

import csv
import json
import sys


def data_metro():
    result = {}
    with open('data_metro_20161217.json', 'r', encoding='cp1251') as f:
        # Загружаем json, на выходе список
        metrodata = json.load(f)
        # Внутри каждого элемента списка словарь
        for line in metrodata:
            name = line['Name']
            result[name] = result.setdefault(name, [float(line['Longitude_WGS84']), float(line['Latitude_WGS84'])])
        return result

def data_bus_stop():
    pass

if __name__ == '__main__':
    try:
        metro = data_metro()
        print(metro)
        bus_stop = data_bus_stop()

    except OSError as err:
        print('OS Error: {}'.format(err))
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise
