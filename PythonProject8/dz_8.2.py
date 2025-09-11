class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b


def main():
    calc = Calculator()

    try:
        # Ввод чисел
        #
        num1 = float(input("Введите первое число: "))
        num2 = float(input("Введите второе число: "))

        # Ввод операции
        #
        operation = input("Введите операцию (+, -, *, /): ")

        # Выполнение операции
        #
        if operation == '+':
            result = calc.add(num1, num2)
        elif operation == '-':
            result = calc.subtract(num1, num2)
        elif operation == '*':
            result = calc.multiply(num1, num2)
        elif operation == '/':
            result = calc.divide(num1, num2)
        else:
            raise ValueError("Неверная операция. Используйте +, -, *, /")

        print(f"Результат: {result}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")
    except ZeroDivisionError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Произошла неизвестная ошибка: {e}")


if __name__ == "__main__":
    main()