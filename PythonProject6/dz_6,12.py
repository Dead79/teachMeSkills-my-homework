import random


def find_columns_with_number(matrix, number):
    columns_with = []
    columns_without = []

    for x in range(len(matrix[0])):
        found = False
        for i in range(len(matrix)):
            if matrix[i][x] == number:
                found = True
                break
        if found:
            columns_with.append(x+1)
        else:
            columns_without.append(x+1)

    return columns_with, columns_without


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

print("Матрица:")
for row in matrix:
    print(row)

H = int(input("Введите число H: "))

columns_with, columns_without = find_columns_with_number(matrix, H)

print(f"Столбцы с числом {H}: {columns_with}")
print(f"Столбцы без числа {H}: {columns_without}")