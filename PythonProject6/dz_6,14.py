import random

stroki = int(input("Строки: "))
stolbci = int(input("Столбцы: "))

matrix = []
for i in range(stroki):
    row = []
    for j in range(stolbci):
        row.append(random.randint(0, 1))
    matrix.append(row)

print("Исходная матрица:")
for row in matrix:
    print(row)

new_matrix = []
for row in matrix:
    count_ones = sum(row)
    if count_ones % 2 == 0:
        new_row = row + [0]
    else:
        new_row = row + [1]
    new_matrix.append(new_row)

print("Матрица с добавленным столбцом:")
for row in new_matrix:
    print(row)