from yandex_translate import YandexTranslate, YandexTranslateException

#translate = YandexTranslate('trnsl.1.1.20161206T204246Z.d8c8ef6d545c7ee5.3b96b277a0d9bb5f0a0060714a5b75d6fa6604b3')
try:
    translate = YandexTranslate('123')
    print('Languages:', translate.langs)
    print('Translate directions:', translate.directions)
    print('Detect language:', translate.detect('Привет, мир!'))
    print('Translate:', translate.translate('Привет, мир!', 'ru-en'))  # or just 'en'
except YandexTranslateException:
    print(123)


