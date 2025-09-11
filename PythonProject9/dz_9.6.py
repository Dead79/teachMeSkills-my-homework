def sum_numbers_in_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

            total_sum = 0
            current_number = ''
            prev_char = ''

            for char in content:
                if char == '-' and not current_number and not prev_char.isdigit():
                    current_number = '-'
                elif char.isdigit():
                    current_number += char
                else:
                    if current_number and current_number != '-':
                        total_sum += int(current_number)
                    current_number = ''
                prev_char = char

            if current_number and current_number != '-':
                total_sum += int(current_number)

            print(f"Сумма всех чисел в файле: {total_sum}")

    except FileNotFoundError:
        print(f"Файл {filename} не найден!")


filename = input("Введите название файла: ")
sum_numbers_in_file(filename)