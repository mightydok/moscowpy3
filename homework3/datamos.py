# encoding: utf-8

import csv
import sys

try:
    with open('datamos_20161217.csv', 'r', encoding='cp1251') as f:
#        lines = csv.reader(f, delimiter=',', quotechar='"')
#        for row in lines:
#            print(row)
        lines = csv.DictReader(f, delimiter=';')
        streets = {}
        for line in lines:
            name = line['Street']
            streets[name] = streets.get(name, 0) + 1

        streets_sorted = sorted(streets.items(), key=lambda x: x[1], reverse=True)
        print('Название улицы: {}, количество остановок: {}'.format(streets_sorted[0][0], streets_sorted[0][1]))

except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
