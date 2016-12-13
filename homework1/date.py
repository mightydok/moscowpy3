# encoding: utf-8

from datetime import datetime, timedelta

day_back = timedelta(days=1)
month_back = timedelta(weeks=4)

date_string = '01/01/17 12:10:03.234567'
date_string_parsed = datetime.strptime(date_string, '%m/%d/%y %H:%M:%S.%f')

print('now: {}'.format(datetime.now()))
print('today is: {}'.format(datetime.date(datetime.now())))
print('yesterday is: {}'.format(datetime.date(datetime.now() - day_back)))
print('month back is: {}'.format(datetime.date(datetime.now() - month_back)))
print('parsed date_string: {} and date from string: {}'.format(date_string_parsed, datetime.date(date_string_parsed)))
