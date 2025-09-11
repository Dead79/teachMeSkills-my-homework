import random


def find_min_max(matrix):

    min_chislo = matrix[0][0]
    max_chislo = matrix[0][0]
    min_index = (0, 0)
    max_index = (0, 0)

    for i in range(len(matrix)):
        for x in range(len(matrix[i])):
            if matrix[i][x] < min_chislo:
                min_chislo = matrix[i][x]
                min_index = (i, x)
            if matrix[i][x] > max_chislo:
                max_chislo = matrix[i][x]
                max_index = (i, x)

    return min_chislo, min_index, max_chislo, max_index


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


min_val, min_index, max_val, max_index = find_min_max(matrix)


print(f"\nМинимальный элемент: {min_val}")
print(f"Индекс минимального элемента: строка {min_index[0]+1}, столбец {min_index[1]+1}")

print(f"\nМаксимальный элемент: {max_val}")
print(f"Индекс максимального элемента: строка {max_index[0]+1}, столбец {max_index[1]+1}")