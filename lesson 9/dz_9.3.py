from collections import Counter
import string


def find_most_common_words(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        for line_num, line in enumerate(infile, 1):
            # Убираем знаки препинания из строки
            translator = str.maketrans('', '', string.punctuation + '«»—…')
            clean_line = line.translate(translator)

            # Разбиваем на слова
            words = clean_line.strip().split()

            if words:
                # Считаем частоту слов
                word_counts = Counter(words)
                # Находим самое частое слово и его количество
                most_common_word, count = word_counts.most_common(1)[0]

                # Записываем только слово и счетчик
                outfile.write(f"{most_common_word} {count}\n")
            else:
                outfile.write("Пустая строка\n")


# Пример использования
input_filename = input("Введите имя входного файла: ")
output_filename = input("Введите имя выходного файла: ")

find_most_common_words(input_filename, output_filename)
print(f"Результат записан в файл {output_filename}")