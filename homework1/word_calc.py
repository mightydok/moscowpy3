# encoding: utf-8

def word_calc(string):
    numbers = {
    'один': '1', 'два': '2', 'три': '3',
    'четыре': '4', 'пять': '5', 'шесть': '6',
    'семь': '7', 'восемь': '8', 'девять': '9',
    'ноль': '0', 'плюс': '+', 'минус': '-',
    'умножить': '*', 'разделить': '/', 'и': '.',
    }

    result = ''

    string = string.lower().strip().replace(' на', '')
    string = string.split(' ')[2:]
    for num in string:
        result += numbers[num]

    return result

if __name__ == '__main__':
    if 'сколько будет четыре и пять умножить на шесть и два'.startswith('сколько будет'):
        print(word_calc('сколько будет четыре и пять умножить на шесть и два'))
