def fibonacci_generator():
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def fibonacci_by_count():
    """Вывод N первых чисел Фибоначчи"""
    try:
        n = int(input("Введите количество чисел Фибоначчи для вывода: "))

        if n <= 0:
            print("Пожалуйста, введите положительное число!")
            return

        print(f"\nПервые {n} чисел последовательности Фибоначчи:")

        fib_gen = fibonacci_generator()

        for i in range(n):
            print(f"{i + 1}: {next(fib_gen)}")

    except ValueError:
        print("Ошибка: введите целое число!")


def fibonacci_by_max_value():
    """Вывод чисел Фибоначчи до заданного значения"""
    try:
        max_value = int(input("Введите максимальное число в последовательности: "))

        if max_value < 0:
            print("Пожалуйста, введите неотрицательное число!")
            return

        print(f"\nЧисла Фибоначчи до {max_value}:")

        fib_gen = fibonacci_generator()
        fib_number = next(fib_gen)

        while fib_number <= max_value:
            print(fib_number)
            fib_number = next(fib_gen)

    except ValueError:
        print("Ошибка: введите целое число!")


def menu():
    """Меню программы"""
    while True:
        print("\n" + "=" * 40)
        print("ПОСЛЕДОВАТЕЛЬНОСТЬ ЧИСЕЛ ФИБОНАЧЧИ")
        print("=" * 40)
        print("1. Вывести N первых чисел")
        print("2. Вывести числа до заданного значения")
        print("3. Выйти")
        print("=" * 40)

        choice = input("Выберите действие (1-3): ")

        if choice == '1':
            fibonacci_by_count()
        elif choice == '2':
            fibonacci_by_max_value()
        elif choice == '3':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    menu()