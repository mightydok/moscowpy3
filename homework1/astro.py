# encoding: utf-8

import ephem

def astro_full_moon(day):
    day = day.lower().replace('?', '').split(' ')[-1]
    return ephem.next_full_moon(day)

if __name__ == '__main__':
    print(astro_full_moon('Когда ближайшее полнолуние после 2016-10-01?'))
