# encoding: utf-8

import csv
import json
import sys

def extract_data(filename, encoding, type):
    result = {}
    with open(filename, 'r', encoding=encoding) as f:
        if type == 'json':
            data = json.load(f)
        elif type == 'csv':
            data = csv.DictReader(f, delimiter=';')
        else:
            return 'Неподдерживаемый тип данных'

        for line in data:
            name = line['Name']
            result[name] = result.setdefault(name, [float(line['Longitude_WGS84']), float(line['Latitude_WGS84'])])
        return result

if __name__ == '__main__':
    try:
        metro = extract_data('data_metro_20161217.json', 'cp1251', 'json')
        bus_stop = extract_data('datamos_20161217.csv', 'cp1251', 'csv')
        print(metro, bus_stop)

    except OSError as err:
        print('OS Error: {}'.format(err))
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise
