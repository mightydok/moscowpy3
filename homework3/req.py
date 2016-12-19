# encoding: utf-8

import requests
import json

def get_weather(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    else:
        return('Не могу получить данные о погоде!')

if __name__ == '__main__':
    print(get_weather('http://api.openweathermap.org/data/2.5/weather?id=524901&units=metric&APPID=2853a176be5333d336775ad3cfb4027b'))
