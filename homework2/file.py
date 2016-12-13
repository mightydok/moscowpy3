# encoding: utf-8

with open(file='referat.txt', mode='r', encoding='utf-8') as f:
    numwords = 0
    for line in f:
        line = line.replace('\n', '').split(' ')
        if not line[0] == '':
            numwords += len(line)

    print('Количество слов в тексте: {}'.format(numwords))
