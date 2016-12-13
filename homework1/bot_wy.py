# coding: utf-8

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from yandex_translate import YandexTranslate, YandexTranslateException
from botdb import citydblist

import ephem
import random

def main():
    updater = Updater("278875881:AAE_qMeNfatAqkML4JQF6YZ3rCcJ79hjE4I")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("tr", translate_word, pass_args=True))
    dp.add_handler(CommandHandler("wordcount", word_count, pass_args=True))
    dp.add_handler(CommandHandler("goroda", goroda, pass_args=True, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))

    dp.add_error_handler(show_error)

    updater.start_polling()
    updater.idle()

def greet_user(bot, update):
    print("Вызван /start")
    custom_keyboard = [
                        ['1', '2', '3', '+'],
                        ['4', '5', '6', '-'],
                        ['7', '8', '9', '*'],
                        ['.', '0', '=', ':'],
                    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(update.message.chat_id, text='Привет, я умный бот, могу переводить с русского '
                                                 'на аглийский и обратно, набери команду /tr <слово> '
                                                 'для перевода \n'
                                                 'Также умею считать простые арифметические примеры '
                                                 'из строки которая заканчивается на = \n'
                                                 'Для калькулатора есть удобная клавиатура \n'
                                                 'Можно поиграть в города, набери /goroda название_города '
                                                 'или /goroda заново для перезапуска игры \n', reply_markup=reply_markup)

def show_error(bot, update, error):
    print('Update "{} caused error "{}"'.format(update, error))

def talk_to_me(bot, update, user_data):
    print('Пришло сообщение: "{}"'.format(update.message.text))

    # Обрабатываем пришедший текст
    message = update.message.text.strip()
    # Проверяем пришел ли запрос на калькулятор c = на конце
    if not message.startswith('=') and message.endswith('='):
        message = message.replace(' ', '')
        result = calculate(message)
        bot.sendMessage(update.message.chat_id, 'Результат выражения: {}'.format(result))
    # Проверям пришел ли запрос с клавиатуры
    elif message in '0123456789+-*:.=':
        message = message.replace(' ', '')
        # Заменяем : на /, символ / - телеграм не передает
        if message == ':':
            message = message.replace(':','/')
        user_data['calc'] = user_data.get('calc', '') + message
        # Если пришло = - отдаем результат и обнуляем словарь
        if message == '=':
            result = calculate(user_data['calc'])
            bot.sendMessage(update.message.chat_id, 'Результат выражения: {}'.format(result))
            user_data['calc'] = ''
    # Проверяем пришел ли запрос для словестного калькулятора
    elif message.lower().strip().startswith('сколько будет'):
        result = calculate(word_calc(message))
        bot.sendMessage(update.message.chat_id, 'Результат выражения: {}'.format(result))
    elif message.lower().strip().startswith('когда ближайшее полнолуние после'):
        result = astro_full_moon(message)
        bot.sendMessage(update.message.chat_id, 'Ближайшее полнолуние будет: {}'.format(result))
    else:
        # Если не режим калькулятора, то пишем в ответ текст который пришел
        bot.sendMessage(update.message.chat_id, update.message.text)

def translate_word(bot, update, args):
    print('Пришло слово для перевода: "{}"'.format(args))

    try:
        # Подключаемся к Яндекс переводчику
        translate = YandexTranslate(
            'trnsl.1.1.20161206T204246Z.d8c8ef6d545c7ee5.3b96b277a0d9bb5f0a0060714a5b75d6fa6604b3')

        # Получаем слово для перевода, телеграм нам дает список, собираем его в строку
        word = ' '.join(args).lower()
        # Определяем язык слова
        word_lang = translate.detect(word)

        # Если язык непонятный, пишем в чат что его не поддерживаем
        if word_lang not in ['ru', 'en']:
            bot.sendMessage(update.message.chat_id, 'Я знаю только русский и английский')
            return
        # Выбираем язык в какой требуется перевод
        elif word_lang == 'ru':
            lang = 'en'
        else:
            lang = 'ru'

        # Переводим и на выходе получаем словарь
        word_translated_dic = translate.translate(word, lang)
        # Проверяем что полученный словарь содержит перевод и это строка
        if word_translated_dic['text'][0] and isinstance(word_translated_dic['text'][0], str):
            # Пишем в чат перевод из словара выбираем список по ключу text
            bot.sendMessage(update.message.chat_id, 'Перевод: {}'.format(word_translated_dic['text'][0]))
        # Иначе поднимаем ошибку с кодом 422
        else:
            raise YandexTranslateException(422)

    # Если возникли проблемы с переводом, пишем про это
    except YandexTranslateException:
        bot.sendMessage(update.message.chat_id, 'Не смог перевести слово. Или слово такое, что Яндекс его перевести '
                        'не может, или просто недоступно API для перевода')

def word_count(bot, update, args):
    print('Пришла строка для подсчета: "{}"'.format(args))
    # Создаем список для подсчета количества слов
    numwords = []
    spec_symbols = '~`@#$%^&*()_-=!?\';[]\{\}<>,.*/+\\'

    # Проходим список слов в цикле, убираем спецсимволы и проверяем слово ли нам передали, если да - добавляем
    # в массив для подсчета
    for word in args:
        if word.strip().replace('\"', '').isalpha() == True:
            numwords.append(word)
    bot.sendMessage(update.message.chat_id, 'Количество слов в строке: {}'.format(len(numwords)))


def calculate(string):
    try:
        string = string.lower().replace('=', '')
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

def word_calc(string):
    print('Пришла строка для подсчета: "{}"'.format(string))
    # Словарь цифр
    numbers = {
    'один': '1', 'два': '2', 'три': '3',
    'четыре': '4', 'пять': '5', 'шесть': '6',
    'семь': '7', 'восемь': '8', 'девять': '9',
    'ноль': '0', 'плюс': '+', 'минус': '-',
    'умножить': '*', 'разделить': '/', 'и': '.',
    }
    # Строка результата
    result = ''
    # Обрабатываем строку, удаляем ненужный предлог
    string = string.lower().strip().replace(' на', '')
    # Убираем фразу - сколько будет, все остальное добавляем в список
    string = string.split(' ')[2:]
    # Собираем строку для рассчета
    for num in string:
        result += numbers[num]

    return result

def astro_full_moon(day):
    day = day.lower().replace('?', '').split(' ')[-1]
    return ephem.next_full_moon(day)

def goroda(bot, update, args, user_data):
    print('Пришла строка для игры в города: "{}"'.format(args))

    # Vars
    next_gorod_letter = ''
    letter = -1

    # Получаем строку из списка аргуметов от пользователя
    user_input = args[0].lower().strip()

    # Перезапуск игры
    if user_input == 'заново':
        bot.sendMessage(update.message.chat_id, 'Пересоздал список городов, играем дальше')
        # Наполняем список в пользовательском словаре
        user_data['cities'] = citydblist[:]
        return
    else:
        # Получаем в словаре user_data список городов, если такого ключа нет, наполняем его
        user_data['cities'] = user_data.get('cities', citydblist[:])

    # Если список городов пустой, пишем пользователю
    if len(user_data['cities']) == 0:
        bot.sendMessage(update.message.chat_id, 'Города кончились, бот больше не знает!')
        return

    # Если пользователь передал несколько городов, пишем об этом
    if len(args) > 1:
        bot.sendMessage(update.message.chat_id, 'В строке должен быть только один город!')
        return

    # Если введеный город есть в списке, получаем его последнюю букву
    if user_input in user_data['cities']:
        next_gorod_letter = user_input[letter]
        # Если буква не может быть в начале названия города то выбираем следующую
        while next_gorod_letter in 'ъьы':
            letter -= 1
            next_gorod_letter = user_input[letter]
        # Удаляем использованный город из списка
        user_data['cities'].remove(user_input)

        # Если первая буква города найдена в списке городов, выводим его
        city_for_random = []
        for city in user_data['cities']:
            if city.startswith(next_gorod_letter):
                city_for_random.append(city)

        # Выводим случайный город из базы по найденной букве, так интереснее
        if len(city_for_random) > 0:
            result = random.choice(city_for_random)
            add_message = ''
        # Или выводим случайныйы город
        else:
            result = random.choice(user_data['cities'])
            add_message = 'Не нашел города на эту букву, выбрал случайный: '

        bot.sendMessage(update.message.chat_id, add_message + '{}, ваш ход'.format(result.capitalize()))
        # Удаляем использованный город из списка
        user_data['cities'].remove(result)
        return

    else:
        bot.sendMessage(update.message.chat_id, 'Город: {} уже был или нет такого города в природе'.format(user_input))
        return

if __name__ == "__main__":
    main()
