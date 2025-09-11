def caesar_encrypt(text, shift, alphabet):
    """Шифрует текст шифром Цезаря с заданным сдвигом для указанного алфавита"""
    encrypted = ''
    for char in text:
        if char in alphabet:
            # Находим индекс символа в алфавите
            #
            index = alphabet.index(char)
            # Вычисляем новый индекс со сдвигом
            #
            new_index = (index + shift) % len(alphabet)
            encrypted += alphabet[new_index]
        elif char.lower() in alphabet:
            # Обрабатываем заглавные буквы
            #
            lower_char = char.lower()
            index = alphabet.index(lower_char)
            new_index = (index + shift) % len(alphabet)
            encrypted += alphabet[new_index].upper()
        else:
            # Не буквенные символы остаются без изменений
            #
            encrypted += char
    return encrypted


def detect_alphabet(text):
    """Определяет алфавит текста (русский или английский)"""
    russian_chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    english_chars = 'abcdefghijklmnopqrstuvwxyz'

    for char in text.lower():
        if char in russian_chars:
            return 'russian'
        elif char in english_chars:
            return 'english'


def encrypt_file(input_filename, output_filename):
    #Шифрует файл с разным сдвигом для каждой строки
    #
    try:
        # Алфавиты
        russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        english_alphabet = 'abcdefghijklmnopqrstuvwxyz'

        with open(input_filename, 'r', encoding='utf-8') as infile, \
                open(output_filename, 'w', encoding='utf-8') as outfile:

            line_number = 1
            for line in infile:
                line_content = line.rstrip('\n')
                # Определяем алфавит для текущей строки
                #
                alphabet_type = detect_alphabet(line_content)
                alphabet = russian_alphabet if alphabet_type == 'russian' else english_alphabet

                # Шифруем строку
                #
                encrypted_line = caesar_encrypt(line_content, line_number, alphabet)
                outfile.write(encrypted_line + '\n')
                line_number += 1

        print(f"Файл успешно зашифрован и сохранен как {output_filename}")

    except FileNotFoundError:
        print(f"Файл {input_filename} не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Основная программа
#
input_file = input("Введите имя входного файла: ")
output_file = input("Введите имя выходного файла: ")

encrypt_file(input_file, output_file)