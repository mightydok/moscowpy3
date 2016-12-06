name_list = ["Вася", "Маша", "Петя", "Валера", "Саша", "Даша"]

answer_list = {
    'ты кто?': 'Дед Пихто!',
    'что делаешь?': 'Сижу в чатике, курю кальян',
    'норм': 'Ну и отлично, у меня то же все норм'
}

def find_person(name):
    while True:
        item = name_list.pop()
        if name == item:
            return name
            break

def ask_user():
    try:
        while True:
            question = input('Как дела?: ').lower().strip()
            if question in ['хорошо', 'пока']:
                print('Пока, удачного дня тебе!')
                break
            else:
                print(get_answer(question))
    except (KeyboardInterrupt, EOFError):
        print('\nИсключение обработано, выходим!')

def get_answer(question):
    return answer_list.get(question, 'Я не понимаю тебя')

if __name__ == '__main__':
    ask_user()

