# encoding: utf-8

def goroda(args):
    cities = [ 'москва', 'самара', 'архангельск', 'коломна' ]
    next_gorod_letter = ''
    gorod = gorod.lower().strip()

    if len(args) > 1:
        return 'Должен быть один город'

    if gorod in cities:
        next_gorod_letter = gorod[-1]
        cities.remove(gorod)

    for city in cities:
        if city.startswith(next_gorod_letter):
            cities.remove(city)
            return city


if __name__ == '__main__':
    goroda(['Москва'])
