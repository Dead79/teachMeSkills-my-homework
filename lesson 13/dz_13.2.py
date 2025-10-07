def cyclic_sequence_generator(sequence):
    """Генератор бесконечной циклической последовательности"""
    index = 0
    while True:
        yield sequence[index]
        index = (index + 1) % len(sequence)


def main():
    """Основная функция программы"""
    try:
        # Ввод последовательности от пользователя
        sequence_input = input("Введите последовательность чисел через пробел: ")
        sequence = [int(x) for x in sequence_input.split()]

        if not sequence:
            print("Ошибка: последовательность не может быть пустой!")
            return

        # Ввод количества чисел для вывода
        n = int(input("Введите количество чисел для вывода: "))

        if n <= 0:
            print("Пожалуйста, введите положительное число!")
            return

        print(f"\nПервые {n} чисел циклической последовательности:")

        # Создаем генератор
        gen = cyclic_sequence_generator(sequence)

        # Выводим n чисел
        for i in range(n):
            print(f"{i + 1}: {next(gen)}")

    except ValueError:
        print("Ошибка: введите корректные числа!")


def menu():
    """Меню программы"""
    while True:
        print("\n" + "=" * 50)
        print("ЦИКЛИЧЕСКАЯ ПОСЛЕДОВАТЕЛЬНОСТЬ ЧИСЕЛ")
        print("=" * 50)
        print("1. Создать циклическую последовательность")
        print("2. Выйти")
        print("=" * 50)

        choice = input("Выберите действие (1-2): ")

        if choice == '1':
            main()
        elif choice == '2':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    menu()