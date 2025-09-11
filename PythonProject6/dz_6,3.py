import random


number = random.randint(1, 19)
print("Исходное число:", number)


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


if is_prime(number):
    print(f"{number} - простое число")
else:
    print(f"{number} - не является простым числом")