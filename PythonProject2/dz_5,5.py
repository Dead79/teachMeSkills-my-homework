import random

r_int = [random.randint(1, 10) for _ in range(15)]

print(r_int)


def check_unique_numbers(numbers):
    from collections import defaultdict
    count_dict = defaultdict(int)
    for num in numbers:
        count_dict[num] += 1

    duplicates = {num: count for num, count in count_dict.items() if count > 1}

    if not duplicates:
        print("Все числа в списке уникальны.")
    else:
        print("Не все числа уникальны. Дубликаты:")
        for num,  count in duplicates.items():
            print(f"Число {num} повторяется {count} раз(а)")


check_unique_numbers(r_int)