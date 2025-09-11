import re


def censor_text(input_filename):
    # Читаем запрещенные слова из файла
    try:
        with open('stop_words.txt', 'r', encoding='utf-8') as f:
            stop_words = f.read().split()
    except FileNotFoundError:
        print("Файл stop_words.txt не найден!")
        return

    # Читаем содержимое файла для цензуры
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Файл {input_filename} не найден!")
        return

    # Заменяем запрещенные слова на звездочки (независимо от регистра)
    for word in stop_words:
        # Создаем регулярное выражение для поиска слова в любом регистре
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        # Заменяем на звездочки той же длины
        text = pattern.sub('*' * len(word), text)

    # Выводим результат
    print(text)


# Основная программа
filename = input("Введите название текстового файла: ")
censor_text(filename)