import random


r_int = [random.randint(1, 15) for _ in range(15)]
print("Исходный список:", r_int)


numbers = r_int
numbers.sort()
print("Отсортированный список:", numbers)


def binary_search(sorted_list, target):
    left = 0
    right = len(sorted_list) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_list[mid] == target:
            return mid
        elif sorted_list[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1



try:
    target_value = int(input("Введите число для поиска: "))
    position = binary_search(numbers, target_value)

    if position != -1:
        print(f"Позиция элемента {target_value} в списке: {position}")
    else:
        print(f"Элемент {target_value} не найден в списке.")
except ValueError:
    print("Ошибка: введите целое число!")