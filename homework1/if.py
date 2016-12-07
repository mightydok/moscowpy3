def string_compare(string1, string2):
    try:
        if len(string1) == 0 or len(string2) == 0:
            return "Строки не могут быть пустыми"
        elif string1 == string2:
            return 1
        elif string1 != string2:
            if string2 == "learn":
                return 3
            elif len(string1) > len(string2):
                return 2
            else:
                return "Строки не попали ни под одно условие сравнения"
    except TypeError:
        return "Проверьте значения, должны быть строки"

if __name__ == "__main__":
    try:
        print(string_compare("string11", "string111"))
    except TypeError as e:
        print("Возникла ошибка в ходе выполнения: {}".format(e))
