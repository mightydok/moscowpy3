# encoding: utf-8

import csv
import json
import sys
from vincenty import vincenty

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
        uniq = {}
        metro = extract_data('data_metro_20161217.json', 'cp1251', 'json')
        bus = extract_data('datamos_20161217.csv', 'cp1251', 'csv')
        for metro_station in metro:
            for bus_station in bus:
                if vincenty(metro[metro_station], bus[bus_station]) <= 0.5:
                    uniq[metro_station] = uniq.get(metro_station, 0) + 1

        metro_station_sorted = sorted(uniq.items(), key=lambda x: x[1], reverse=True)
        print('Станция метро: {}, количество остановок в радиусе 0.5км: {}'.format(metro_station_sorted[0][0], metro_station_sorted[0][1]))

    except OSError as err:
        print('OS Error: {}'.format(err))
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise
