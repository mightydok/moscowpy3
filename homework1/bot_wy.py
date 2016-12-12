# coding: utf-8

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from yandex_translate import YandexTranslate, YandexTranslateException

import re

spec_symbols = '~`@#$%^&*()_-=!?\';[]\{\}<>,.*/+\\'

def main():
    updater = Updater("278875881:AAE_qMeNfatAqkML4JQF6YZ3rCcJ79hjE4I")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("tr", translate_word, pass_args=True))
    dp.add_handler(CommandHandler("wordcount", word_count, pass_args=True))
    dp.add_handler(MessageHandler([Filters.text], talk_to_me))

    dp.add_error_handler(show_error)

    updater.start_polling()
    updater.idle()

def greet_user(bot, update):
    print("Вызван /start")
    bot.sendMessage(update.message.chat_id, text='Привет, я умный бот, могу переводить с русского на аглийский и '
                                                 'обратно, набери команду /tr <слово> для перевода '
                                                 'Также умею считать простые арифметические примеры из строки которая заканчивается на = ')

def show_error(bot, update, error):
    print('Update "{} caused error "{}"'.format(update, error))

# Проверка корректной строки для калькулятора
def check_arifmetic_string(bot, update, message):
    if re.findall(r'((?![\+\-\*\/\.\d+\(\)\=]).)', message):
        bot.sendMessage(update.message.chat_id, 'В строке для калькулятора есть лишние символы, '
                                                'удалите их для корректной работы арифметических функций')
        return False
    elif len(re.findall(r'\d+\.\d+|\d+|[\+\-\*\/\(\)]', message)) < 3:
        bot.sendMessage(update.message.chat_id, 'Невозможно обработать запрос, не хватает всех цифр или арифметических знаков')
        return False
    elif len(re.findall(r'[\+\-\*\/]', message)) == 0 or len(re.findall(r'\d+\.\d+|\d+', message)) == 0:
        bot.sendMessage(update.message.chat_id, 'В строке не найдены арифметические знаки или цифры, калькулятор не может работать без них')
        return False
    elif len(re.findall(r'\d+\.\d+|\d+', message)) == 1:
        bot.sendMessage(update.message.chat_id, 'Нужна еще одна цифра для работы калькулятора')
        return False
    elif '**' in message or '//' in message:
        bot.sendMessage(update.message.chat_id, 'Арифметические действия: ** и // не поддерживаются')
        return False
    else:
        return True

def talk_to_me(bot, update):
    print('Пришло сообщение: "{}"'.format(update.message.text))

    # Обрабатываем пришедший текст
    message = update.message.text.strip().replace(' ', '')
    # Проверяем пришел ли запрос на калькулятор
    if not message.startswith('=') and message.endswith('='):
        # Проверям строку для калькулятора на корректный текст
        if check_arifmetic_string(bot, update, message):
            try:
                # Собираем строку для рассчета
                calculated = re.findall(r'[\+\-\*\/\d+\(\)\.]', message)
                # Считаем и отдаем результат
                result = eval(''.join(calculated))
                bot.sendMessage(update.message.chat_id, result)
                return
            except SyntaxError:
                bot.sendMessage(update.message.chat_id, 'Ошибка в примере, калькулятор не может выполнить арифметическое действие')
                return
            except ZeroDivisionError:
                bot.sendMessage(update.message.chat_id, 'На ноль делить нельзя')
                return
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
    # Проходим список слов в цикле, убираем спецсимволы и проверяем слово ли нам передали, если да - добавляем
    # в массив для подсчета
    for word in args:
        if word.strip(spec_symbols).isalpha() == True:
            numwords.append(word)
    bot.sendMessage(update.message.chat_id, 'Количество слов в строке: {}'.format(len(numwords)))

if __name__ == "__main__":
    main()
