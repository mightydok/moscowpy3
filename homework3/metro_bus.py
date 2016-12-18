# encoding: utf-8

import csv
import json
import sys
from vincenty import vincenty
from collections import Counter

def extract_data(filename, encoding='cp1251'):
    result = []
    file_type = filename.split('.')[1]

    with open(filename, 'r', encoding=encoding) as f:
        if file_type == 'json':
            data = json.load(f)
        elif file_type == 'csv':
            data = csv.DictReader(f, delimiter=';')
        else:
            return 'Неподдерживаемый тип данных'

        for line in data:
            result.append(line)

        return result


def agregate_data(data_metro, data_bus):
    print(data_bus)

if __name__ == '__main__':
    try:
        aggregate = {}
        # Парсим файлы
        data_metro = extract_data('data_metro_20161217.json')
        data_bus = extract_data('datamos_20161217.csv')

        # Для каждой станции метро получаем название станции и координаты вестибюлей
        for metro in data_metro:
            metro_name_of_station = metro['NameOfStation']
            metro_position = [float(metro['Longitude_WGS84']), float(metro['Latitude_WGS84'])]
            # Для каждой остановки
            for bus in data_bus:
                bus_global_id = bus['global_id']
                bus_position = [float(bus['Longitude_WGS84']), float(bus['Latitude_WGS84'])]
                # Если расстояние от вестибюля до остановки менее или равно 0.5км
                if vincenty(metro_position, bus_position) <= 0.5:
                    # Наполняем словарь
                    # Получаем значения для станции метро, если в словаре его нет возвращаем пустое множество
                    station_set = aggregate.get(metro_name_of_station, set())
                    # Добавляем в множество идентификатор остановки, множество само следит за уникальностью идентификаторов
                    station_set.add(bus_global_id)
                    # Записываем обновленное множество в словарь
                    aggregate[metro_name_of_station] = station_set

        # Проходим словарь, меняем его значения на длину множества
        for row in aggregate:
            aggregate[row] = len(aggregate[row])

        # Выводим ТОП 5
        c = Counter(aggregate)
        print(c.most_common(5))

    except OSError as err:
        print('OS Error: {}'.format(err))
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise
