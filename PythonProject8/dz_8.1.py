def kalkulitor_imt():
    try:
        ves_input = input("Введите ваш вес (кг): ")
        rost_input = input("Введите ваш рост (см): ")

        if not ves_input.replace('.', '').isdigit():
            raise ValueError("Вес должен быть числом чрез точку, а не буквами или символами")
        if not rost_input.replace('.', '').isdigit():
            raise ValueError("Рост должен быть числом через точку, а не буквами или символами")

        ves = float(ves_input)
        rost = float(rost_input)

        if ves <= 0:
            raise ValueError("Вес не может быть меньше или равен 0")
        if rost <= 0:
            raise ValueError("Рост не может быть меньше или равен 0")
        if ves < 3:
            raise ValueError("Вес не может быть меньше 3 кг")
        if ves > 300:
            raise ValueError("Вес не может быть больше 300 кг")
        if rost > 250:
            raise ValueError("Рост не может быть больше 250 см")
        if rost < 50:
            raise ValueError("Рост не может быть меньше 50 см")

        rost_m = rost / 100
        imt = ves / (rost_m ** 2)

        print(f"\nВаш ИМТ: {imt:.2f}")

        if imt < 16:
            print("Выраженный дефицит массы тела")
        elif 16 <= imt < 18.5:
            print("Недостаточная масса тела")
        elif 18.5 <= imt < 25:
            print("Нормальная масса тела")
        elif 25 <= imt < 30:
            print("Избыточная масса тела")
        elif 30 <= imt < 35:
            print("Ожирение 1 степени")
        elif 35 <= imt < 40:
            print("Ожирение 2 степени")
        elif 40 <= imt < 65:
            print("Ожирение 3 степени")
        else:
            print("Некорректные значения роста или веса")
            print("Или вы не человек)))")

    except ValueError as e:
        print(f"Ошибка: {e}")
    except ZeroDivisionError:
        print("Ошибка: Рост не может быть равен нулю")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


kalkulitor_imt()