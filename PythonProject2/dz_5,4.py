import random

r_int = [random.randint(1, 100) for _ in range(10)]

print(r_int)

numbers = r_int

sum_numbers = 0

max_number = numbers[0]

min_number = numbers[0]

for num in numbers:
    sum_numbers += num
    if num > max_number:
        max_number = num
    if num < min_number:
        min_number = num

print(f"Сумма: {sum_numbers}")
print(f"Максимум: {max_number}")
print(f"Минимум: {min_number}")