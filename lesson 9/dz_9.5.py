def find_low_grades(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            print("Учащиеся с оценкой меньше 3 баллов:")
            print("-" * 40)

            for line in file:
                # Разделяем строку на части
                #
                parts = line.strip().split()

                if len(parts) >= 3:
                    # Предполагаем, что оценка - это последний элемент
                    #
                    surname = parts[0]
                    name = parts[1]
                    try:
                        # пробуем преобразовать оценку в число
                        #
                        grade = float(parts[-1])
                        if grade < 3:
                            print(f"{surname} {name} - {grade}")
                    except ValueError:
                        # Если оценка не число, пропускаем строку
                        #
                        continue

    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Основная программа
#
filename = input("Введите название файла с оценками: ")
find_low_grades(filename)