import random

chisla = int(input("Количество чисел: "))
min_znachenie = int(input("Минимальное значение: "))
max_znachenie = int(input("Максимальное значение: "))

numbers = [random.randint(min_znachenie, max_znachenie) for _ in range(chisla)]
strings = list(map(str, numbers))

print("Числа:", numbers)
print("Строки:", strings)