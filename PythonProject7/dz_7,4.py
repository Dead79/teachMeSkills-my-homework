import random
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Функция {func.__name__} выполнялась {end - start:.6f} секунд")
        return result
    return wrapper

@timer
def filter_positive_numbers(numbers):
    return list(filter(lambda x: x > 0, numbers))

chisla = int(input("Количество чисел: "))
min_znachenie = int(input("Минимальное значение: "))
max_znachenie = int(input("Максимальное значение: "))

numbers = [random.randint(min_znachenie, max_znachenie) for _ in range(chisla)]
positive_numbers = filter_positive_numbers(numbers)

print("Все числа:", numbers)
print("Положительные числа:", positive_numbers)