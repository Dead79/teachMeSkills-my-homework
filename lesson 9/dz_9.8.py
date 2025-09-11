import json
import csv
import os


# Функции для работы с JSON
#
def read_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []


def write_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# Функции для работы с CSV
#
def json_to_csv(json_data, csv_filename):
    if not json_data:
        return

    # Получаем все возможные поля из данных
    #
    all_fields = set()
    for employee in json_data:
        all_fields.update(employee.keys())

    fieldnames = sorted(all_fields)

    with open(csv_filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for employee in json_data:
            # Преобразуем данные для CSV
            csv_employee = employee.copy()

            # Списки в строки с запятыми
            #
            if 'languages' in csv_employee and isinstance(csv_employee['languages'], list):
                csv_employee['languages'] = ', '.join(csv_employee['languages'])

            # Boolean в строки
            #
            if 'car' in csv_employee:
                csv_employee['car'] = str(csv_employee['car'])

            writer.writerow(csv_employee)

    with open(csv_filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for employee in json_data:
            # Преобразуем списки в строки для CSV
            #
            csv_employee = employee.copy()
            if 'languages' in csv_employee and isinstance(csv_employee['languages'], list):
                # Просто соединяем через запятую, без кавычек и скобок
                #
                csv_employee['languages'] = ', '.join(csv_employee['languages'])
            writer.writerow(csv_employee)


def read_csv(csv_filename):
    if os.path.exists(csv_filename):
        with open(csv_filename, 'r', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    return []


def add_to_csv(csv_filename, employee_data):
    # Читаем существующие данные для получения всех полей
    existing_data = read_csv(csv_filename)
    if existing_data:
        all_fields = set(existing_data[0].keys())
        all_fields.update(employee_data.keys())
        fieldnames = sorted(all_fields)
    else:
        fieldnames = sorted(employee_data.keys())

    # Преобразуем списки в строки для CSV (правильно!)
    csv_employee = employee_data.copy()
    if 'languages' in csv_employee and isinstance(csv_employee['languages'], list):
        # Просто соединяем через запятую, без кавычек и скобок
        csv_employee['languages'] = ', '.join(csv_employee['languages'])

    # Преобразуем boolean в строку для CSV
    if 'car' in csv_employee:
        csv_employee['car'] = str(csv_employee['car'])

    # Добавляем нового сотрудника
    #
    with open(csv_filename, 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not existing_data:  # Если файл пустой, пишем заголовок
            writer.writeheader()

        # Заполняем отсутствующие поля пустыми значениями
        #
        row = {field: csv_employee.get(field, '') for field in fieldnames}
        writer.writerow(row)

    # Читаем существующие данные для получения всех полей
    #
    existing_data = read_csv(csv_filename)
    if existing_data:
        all_fields = set(fieldnames)
        for emp in existing_data:
            all_fields.update(emp.keys())
        fieldnames = sorted(all_fields)


# Функции для работы с сотрудниками
#
def add_employee(json_filename, csv_filename):
    print("\nДобавление нового сотрудника:")
    name = input("Имя и фамилия: ")
    birthday = input("Дата рождения (дд.мм.гггг): ")
    height = float(input("Рост: "))
    weight = float(input("Вес: "))
    car = input("Есть машина (да/нет): ").lower() == 'да'
    languages = input("Языки программирования (через запятую): ").split(',')
    languages = [lang.strip() for lang in languages]

    employee = {
        'name': name,
        'birthday': birthday,
        'height': height,
        'weight': weight,
        'car': car,
        'languages': languages
    }

    # Добавляем в JSON
    #
    data = read_json(json_filename)
    data.append(employee)
    write_json(json_filename, data)

    # Добавляем в CSV
    #
    add_to_csv(csv_filename, employee)
    print("Сотрудник добавлен!")


def find_employee_by_name(csv_filename):
    name_to_find = input("Введите имя для поиска: ")
    employees = read_csv(csv_filename)

    found = False
    for emp in employees:
        if emp['name'].lower() == name_to_find.lower():
            print(f"\nНайден сотрудник:")
            for key, value in emp.items():
                print(f"{key}: {value}")
            found = True
            break

    if not found:
        print("Сотрудник с таким именем не найден.")


def filter_by_language(csv_filename):
    language = input("Введите язык программирования: ").strip().lower()
    employees = read_csv(csv_filename)

    found = False
    print(f"\nСотрудники, владеющие {language}:")
    for emp in employees:
        emp_languages = emp.get('languages', '')
        if emp_languages:
            # Убираем пробелы и разделяем по запятым
            #
            languages_list = [lang.strip().lower() for lang in emp_languages.split(',')]
            # Ищем точное совпадение
            #
            if language in languages_list:
                # Выводим только имя сотрудника без лишних символов
                # #
                print(f"{emp['name']}")
                found = True

    if not found:
        print("Сотрудников с таким языком не найдено.")
        print("Доступные языки в базе:")
        all_languages = set()
        for emp in employees:
            if emp.get('languages'):
                langs = [lang.strip().lower() for lang in emp['languages'].split(',')]
                all_languages.update(langs)
        if all_languages:
            # Выводим языки через запятую без кавычек и скобок
            #
            print(", ".join(sorted(all_languages)))

def filter_by_year(csv_filename):
    try:
        year = int(input("Введите год рождения для фильтра: "))
        employees = read_csv(csv_filename)

        total_height = 0
        count = 0

        for emp in employees:
            birthday = emp.get('birthday', '')
            if birthday:
                try:
                    # Извлекаем год из даты "дд.мм.гггг"
                    #
                    birth_year = int(birthday.split('.')[2])
                    if birth_year < year:
                        total_height += float(emp.get('height', 0))
                        count += 1
                except (ValueError, IndexError):
                    # Пропускаем некорректные даты
                    #
                    continue

        if count > 0:
            average_height = total_height / count
            print(f"Средний рост сотрудников, родившихся до {year} года: {average_height:.2f}")
        else:
            print("Сотрудников, родившихся до указанного года, не найдено.")

    except ValueError:
        print("Ошибка: введите корректный год.")


# Основное меню
#
def main_menu():
    json_file = "employees.json"
    csv_file = "employees.csv"

    # Инициализация файлов, если их нет
    #
    if not os.path.exists(json_file):
        write_json(json_file, [])
    if not os.path.exists(csv_file):
        json_to_csv(read_json(json_file), csv_file)

    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ УПРАВЛЕНИЯ СОТРУДНИКАМИ")
        print("=" * 50)
        print("1. Добавить нового сотрудника")
        print("2. Найти сотрудника по имени")
        print("3. Фильтр по языку программирования")
        print("4. Фильтр по году рождения")
        print("5. Конвертировать JSON в CSV")
        print("6. Выйти из программы")
        print("=" * 50)

        choice = input("Выберите действие (1-6): ")

        if choice == '1':
            add_employee(json_file, csv_file)
        elif choice == '2':
            find_employee_by_name(csv_file)
        elif choice == '3':
            filter_by_language(csv_file)
        elif choice == '4':
            filter_by_year(csv_file)
        elif choice == '5':
            json_to_csv(read_json(json_file), csv_file)
            print("Данные конвертированы из JSON в CSV")
        elif choice == '6':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


# Запуск программы
#
if __name__ == "__main__":
    main_menu()