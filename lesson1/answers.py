a = {"привет": "И тебе привет!", "как дела": "Лучше всех", "пока": "Увидимся"}
b = input('name: ')

def get_answer(key, dict):
    return a.get(key, 'Строка не найдена в словаре')

print(get_answer(b.lower(), a))