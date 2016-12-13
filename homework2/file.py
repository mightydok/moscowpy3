# encoding: utf-8

import sys

try:
    with open(file='referat.txt', mode='r', encoding='utf-8') as f:
        numwords = 0
        for line in f:
            line = line.replace('\n', '').split(' ')
            if not line[0] == '':
                numwords += len(line)

        print('Количество слов в тексте: {}'.format(numwords))
except OSError as err:
    print("OS error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
