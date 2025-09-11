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

total_sum = 0
for row in matrix:
    for element in row:
        total_sum += element

print(f"\nОбщая сумма всех элементов: {total_sum}")

col_sums = [0] * stolbci
for row in matrix:
    for x in range(stolbci):
        col_sums[x] += row[x]

print("\nСуммы и доли по столбцам:")
for x in range(stolbci):
    percent = (col_sums[x] / total_sum) * 100
    print(f"Столбец {x + 1}: сумма = {col_sums[x]}, доля = {percent:.2f}%")