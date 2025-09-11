letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
shift = 3

while True:
    print("\nВыберите:")
    print("1 - Шифровать")
    print("2 - Дешифровать")
    print("3 - закончить")

    choice = input("Сделайте выбор: ")

    if choice == '3':
        print("Всего хорошего!")
        break

    if choice in ['1', '2']:
        text = input("введите текст: ")
        result = ''

        for char in text:
            if char.lower() in letters:
                index = letters.index(char.lower())
                if choice == '1':
                    new_index = (index + shift) % len(letters)
                else:
                    new_index = (index - shift) % len(letters)

                if char.isupper():
                    result += letters[new_index].upper()
                else:
                    result += letters[new_index]
            else:
                result += char

        print("Результат:", result)

    else:
        print("Выберите цифру!")