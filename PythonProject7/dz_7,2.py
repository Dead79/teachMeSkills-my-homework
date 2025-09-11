import random

chisla = int(input("Количество чисел: "))
min_znachenie = int(input("Минимальное значение: "))
max_znachenie = int(input("Максимальное значение: "))

numbers = [random.randint(min_znachenie, max_znachenie) for _ in range(chisla)]
positive_numbers = list(filter(lambda x: x > 0, numbers))

print("Все числа:", numbers)
print("Положительные числа:", positive_numbers)