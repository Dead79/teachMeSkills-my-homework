import random


r_int = [random.randint(1, 100) for _ in range(10)]
print("Исходный список:", r_int)


numbers = r_int
numbers.sort()
print("Отсортированный список:", numbers)

def binary_search(arr, target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1

    if low > high:
        return -1

    mid = (low + high) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid + 1, high)
    else:
        return binary_search(arr, target, low, mid - 1)


sorted_list = numbers
target = int(input("укажите число позицию которого в списке мы ищем:"))

position = binary_search(sorted_list, target)
print(f"Позиция элемента {target} в списке: {position}")