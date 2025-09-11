import random

stroki = int(input("Строки: "))
stolbci = int(input("Столбцы: "))
min_znachenie = int(input("Минимум: "))
max_znachenie = int(input("Максимум: "))

matrix = []
for i in range(stroki):
    row = []
    for x in range(stolbci):
        row.append(random.randint(min_znachenie, max_znachenie))
    matrix.append(row)

print(f"\nМатрица {stroki}x{stolbci}:")
for row in matrix:
    print(row)