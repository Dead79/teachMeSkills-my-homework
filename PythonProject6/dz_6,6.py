alfavit = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

while True:
    print("\nЧто делать?")
    print("1 - Зашифровать текст")
    print("2 - Расшифровать текст")
    print("3 - Выйти")

    choise = input("Введите цифру: ")

    if choise == '3':
        print("Программа завершена!")
        break

    if choise == '1' or choise == '2':
        text = input("Введите текст: ")
        key = input("Введите ключ (слово): ").lower()

        new_key = ''
        for letter in key:
            if letter in alfavit:
                new_key += letter

        if new_key == '':
            print("Ошибка! Ключ должен содержать русские буквы")
            continue

        result = ''
        number_letter_key = 0

        for simbol in text:
            if simbol.lower() in alfavit:
                number_letter = alfavit.index(simbol.lower())

                letter_key = new_key[number_letter_key % len(new_key)]
                sdvig = alfavit.index(letter_key)

                if choise == '1':
                    new_number = (number_letter + sdvig) % len(alfavit)
                else:
                    new_number = (number_letter - sdvig) % len(alfavit)

                if simbol.isupper():
                    result += alfavit[new_number].upper()
                else:
                    result += alfavit[new_number]

                number_letter_key += 1
            else:

                result += simbol

        print("Получилось:", result)

    else:
        print("Неправильный выбор! Введите 1, 2 или 3")