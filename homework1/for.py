# Список с оценками по школе
scores_list = [{'school_class': '1a', 'scores': [3, 3, 5, 5, 3]},
               {'school_class': '2b', 'scores': [2, 3, 4, 5, 2, 5, 4, 3]},
               {'school_class': '2c', 'scores': [3, 2, 2, 3, 2, 2, 3, 4, 4]},
               {'school_class': '3a', 'scores': [5, 5, 4, 2]}]

# Сумма баллов по школе
scores_sum = 0
# Количество оценок по школе
scores_num = 0

# В цикле проходим список, достаем словари
for line in scores_list:
    # Получаем имя класса
    class_name = line['school_class']
    # Получаем список с оценками
    class_scores = line['scores']
    # Получаем сумму оценок по классу
    class_scores_sum = sum(line['scores'])
    # Получаем количество оценок, сразу в float
    class_scores_num = float(len(line['scores']))
    # Получаем среднее по классу и сразу округляем
    class_scores_sum_average = round(class_scores_sum/class_scores_num, 1)

    # Добавляем сумму оценок по классу и количество оценок в глобальные переменные для рассчета данных по школе
    scores_sum += class_scores_sum
    scores_num += class_scores_num

    print('Класс: {}, средний балл: {}'.format(class_name, class_scores_sum_average))

# Считаем среднее по школе
school_scores_average = round(scores_sum/scores_num, 1)

print('-' * 28)
print('Средний балл по школе: {}'.format(school_scores_average))

