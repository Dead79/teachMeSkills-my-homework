#import random


#number = random.randint(1, 128)
#print("Исходное число:", number)
number = int(input("введите десятичное число:"))
def decimal_to_binary_iterative(number):
    if number == 0:
        return "0"
    binary = ""
    while number > 0:
        binary = str(number % 2) + binary
        number = number // 2
    return binary

binary = decimal_to_binary_iterative(number)
print(f"Число {number} в двоичной системе: {binary}")