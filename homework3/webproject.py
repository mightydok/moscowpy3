# encoding: utf-8

from flask import Flask, abort, request, render_template

from req import get_weather, get_names
from datetime import datetime
from news_list import all_news

city_id = 524901
apikey = '2853a176be5333d336775ad3cfb4027b'

app = Flask(__name__)

@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?id=%s&units=metric&APPID=%s' % (city_id, apikey)
    weather = get_weather(url)
    cur_date = datetime.strftime(datetime.now(), '%d.%m.%Y')

    result = '<p><strong>Температура:</strong> %s</p>' % weather['main']['temp']
    result += '<p><strong>Город:</strong> %s</p>' % weather['name']
    result += '<p><strong>Дата:</strong> %s</p>' % cur_date
    return result

@app.route('/news')
def all_the_news():
    colors = ['red', 'green', 'black']
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = 10
    color = request.args.get('color') if request.args.get('color') in colors else 'black'
    return '<h1 style="color: %s">News: <small>%s</small></h1>' % (color, limit)

@app.route('/news/<int:news_id>')
def news_by_id(news_id):
    news_to_show = [news for news in all_news if news['id'] == news_id]
    if len(news_to_show) == 1:
        result = '<h1>%(title)s</h1><p><i>%(date)s</i></p><p>%(text)s</p>'
        result = result % news_to_show[0]
        return result
    else:
        abort(404)

@app.route('/names')
def moscow_names():
    try:
        year = int(request.args.get('year'))
    except:
        year = None

    try:
        names = get_names(year=year)
        return render_template('names.html', names=names)
    except:
        raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=34871, debug=True)
