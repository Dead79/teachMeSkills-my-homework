cf_int = int(input("Последовательность чисел Фибоначи от 0 до "))

x, y = 0, 1
print("будет выглядеть таким образом:")


while x <= cf_int:
    print(x, end = " ")
    x, y = y, x + y