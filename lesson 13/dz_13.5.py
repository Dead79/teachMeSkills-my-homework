from abc import ABC, abstractmethod


# Абстрактный класс стратегии
class MathStrategy(ABC):
    @abstractmethod
    def execute(self, a, b):
        pass


# Конкретные стратегии
class Addition(MathStrategy):
    def execute(self, a, b):
        return a + b


class Subtraction(MathStrategy):
    def execute(self, a, b):
        return a - b


class Multiplication(MathStrategy):
    def execute(self, a, b):
        return a * b


class Division(MathStrategy):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Деление на ноль невозможно!")
        return a / b


# Класс Calculator
class Calculator:
    def __init__(self):
        self._strategy = None

    def set_strategy(self, strategy):
        self._strategy = strategy

    def calculate(self, a, b):
        if self._strategy is None:
            raise ValueError("Стратегия не установлена!")
        return self._strategy.execute(a, b)


def main():
    """Основная функция программы"""
    calculator = Calculator()

    print("=== КАЛЬКУЛЯТОР СО СТРАТЕГИЯМИ ===")

    while True:
        print("\nВыберите операцию:")
        print("1. Сложение")
        print("2. Вычитание")
        print("3. Умножение")
        print("4. Деление")
        print("5. Выйти")

        choice = input("Ваш выбор (1-5): ")

        if choice == '5':
            print("Выход из программы...")
            break

        try:
            a = float(input("Введите первое число: "))
            b = float(input("Введите второе число: "))

            if choice == '1':
                calculator.set_strategy(Addition())
                result = calculator.calculate(a, b)
                print(f"Результат сложения: {a} + {b} = {result}")

            elif choice == '2':
                calculator.set_strategy(Subtraction())
                result = calculator.calculate(a, b)
                print(f"Результат вычитания: {a} - {b} = {result}")

            elif choice == '3':
                calculator.set_strategy(Multiplication())
                result = calculator.calculate(a, b)
                print(f"Результат умножения: {a} × {b} = {result}")

            elif choice == '4':
                calculator.set_strategy(Division())
                result = calculator.calculate(a, b)
                print(f"Результат деления: {a} ÷ {b} = {result}")

            else:
                print("Неверный выбор!")

        except ValueError as e:
            print(f"Ошибка: {e}")
        except ZeroDivisionError:
            print("Ошибка: Деление на ноль!")


# Дополнительная функция для демонстрации смены стратегий
def demonstrate_strategies():
    """Демонстрация работы с разными стратегиями"""
    calculator = Calculator()

    print("\n=== ДЕМОНСТРАЦИЯ СТРАТЕГИЙ ===")

    # Тестовые данные
    numbers = [(10, 5), (8, 2), (15, 3)]

    strategies = [
        ("Сложение", Addition()),
        ("Вычитание", Subtraction()),
        ("Умножение", Multiplication()),
        ("Деление", Division())
    ]

    for a, b in numbers:
        print(f"\nЧисла: {a} и {b}")
        for strategy_name, strategy in strategies:
            calculator.set_strategy(strategy)
            try:
                result = calculator.calculate(a, b)
                print(f"  {strategy_name}: {result}")
            except ValueError as e:
                print(f"  {strategy_name}: {e}")


# Запуск программы
if __name__ == "__main__":
    while True:
        print("\n" + "=" * 40)
        print("ПАТТЕРН 'СТРАТЕГИЯ' - КАЛЬКУЛЯТОР")
        print("=" * 40)
        print("1. Интерактивный калькулятор")
        print("2. Демонстрация стратегий")
        print("3. Выйти")
        print("=" * 40)

        choice = input("Выберите режим (1-3): ")

        if choice == '1':
            main()
        elif choice == '2':
            demonstrate_strategies()
        elif choice == '3':
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")