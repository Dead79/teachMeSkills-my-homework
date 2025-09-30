class Math:
    def __init__(self):
        pass

    def addition(self, a, b):
        result = a + b
        print(f"{a} + {b} = {result}")

    def subtraction(self, a, b):
        result = a - b
        print(f"{a} - {b} = {result}")

    def multiplication(self, a, b):
        result = a * b
        print(f"{a} * {b} = {result}")

    def division(self, a, b):
        if b == 0:
            print("Ошибка: деление на ноль!")
        else:
            result = a / b
            print(f"{a} / {b} = {result}")


# Интерактивное использование
calc = Math()

while True:
    print("\nВыберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Выход")

    choice = input("Ваш выбор (1-5): ")

    if choice == '5':
        break

    try:
        a = float(input("Первое число: "))
        b = float(input("Второе число: "))

        if choice == '1':
            calc.addition(a, b)
        elif choice == '2':
            calc.subtraction(a, b)
        elif choice == '3':
            calc.multiplication(a, b)
        elif choice == '4':
            calc.division(a, b)
        else:
            print("Неверный выбор!")

    except ValueError:
        print("Ошибка: введите числа!")