# encoding: utf-8

def calculate(string):
    try:
        string = string.lower().replace(' ', '')
        parts = string.split('+')

        for plus in range(len(parts)):
            if '-' in parts[plus]:
                parts[plus] = parts[plus].split('-')

        for plus in range(len(parts)):
            parts[plus] = precalculate(parts[plus])

        result = sum(parts)
    except ValueError:
        result = 'Не могу обработать строку для калькулятора'
    except ZeroDivisionError:
        result = 'На ноль делить нельзя'

    return result

def precalculate(part):
    # Если получили строку на вход
    if type(part) is str:
        # Проверяем операция ли это умножения
        if '*' in part:
            result = 1
            # Получаем множители
            for subpart in part.split('*'):
                # Вызываем рекурсию чтобы получить данные в float и выполняем перемножение
                result *= precalculate(subpart)
            return result
        # Проверяем деление ли это
        elif '/' in part:
            # Преобразуем в float числа опять благодаря рекурсии
            parts = list(map(precalculate, part.split('/')))
            # Выделяем целую часть
            result = parts[0]
            # В цикле делим целую часть на дробную
            for subpart in parts[1:]:
                result /= subpart
            return result

        else:
            # Если нам на входе дали строку, но не нашли * или /, то просто возвращаем ту же строку но во float
            return float(part)
    # Если получили список на вход, после второго прохода при определении операции вычитания
    elif type(part) is list:
        # Опять вызываем рекурсию для определения есть ли внутри списка операции умножения и деления
        for i in range(len(part)):
            part[i] = precalculate(part[i])

        # Вычитаем из первого числа сумму остальных чисел в списке
        return part[0]-sum(part[1:])

    return part

if __name__ == '__main__':
    print(calculate('5 + 2 * 3 - 4 - 8 + 11 + 3/2'))
