class BeeElephant:
    def __init__(self, bee_part, elephant_part):
        # Нормализуем суммы частей до 100%
        total = bee_part + elephant_part
        if total > 0:
            self.bee = (bee_part / total) * 100
            self.elephant = (elephant_part / total) * 100
        else:
            self.bee = 50
            self.elephant = 50

    def _get_sound_mix(self):
        """Возвращает смешанный звук в зависимости от процентного соотношения"""
        bee_percent = self.bee

        # Критические точки для звуков (только точные значения)
        if bee_percent == 100:
            return "BZ-ZZ-ZZ-ZZ"  # 100% пчела
        elif bee_percent == 75:
            return "BZ-ZZ-zz-du!"  # 75% пчела
        elif bee_percent == 50:
            return "bz-zz-du-du"  # 50/50
        elif bee_percent == 25:
            return "bz-tu-DU-DU!"  # 25% пчела
        elif bee_percent == 0:
            return "TU-TU-DU-DU"  # 100% слон
        else:
            # Для промежуточных значений находим ближайшую критическую точку
            critical_points = [0, 25, 50, 75, 100]
            closest_point = min(critical_points, key=lambda x: abs(x - bee_percent))

            if closest_point == 100:
                return "BZ-ZZ-ZZ-ZZ"
            elif closest_point == 75:
                return "BZ-ZZ-zz-du!"
            elif closest_point == 50:
                return "bz-zz-du-du"
            elif closest_point == 25:
                return "bz-tu-DU-DU!"
            else:  # 0
                return "TU-TU-DU-DU"

    def fly(self):
        """Возвращает True, если часть пчелы не меньше части слона"""
        return self.bee >= self.elephant

    def trumpet(self):
        """Возвращает смешанный звук в зависимости от соотношения частей"""
        return self._get_sound_mix()

    def eat(self, meal, value):
        """Принимает 'nectar' или 'grass' и изменяет части"""
        if meal not in ["nectar", "grass"]:
            print("Ошибка: meal может быть только 'nectar' или 'grass'")
            return

        value = max(0, value)  # значение не может быть отрицательным

        if meal == "nectar":
            # Увеличиваем пчелу, уменьшаем слона
            new_bee = self.bee + value
            new_elephant = max(0, self.elephant - value)
        else:  # meal == "grass"
            # Увеличиваем слона, уменьшаем пчелу
            new_bee = max(0, self.bee - value)
            new_elephant = self.elephant + value

        # Нормализуем до 100%
        total = new_bee + new_elephant
        if total > 0:
            self.bee = (new_bee / total) * 100
            self.elephant = (new_elephant / total) * 100

    def get_percentages(self):
        """Возвращает процентное соотношение"""
        return f"Пчела: {self.bee:.1f}%, Слон: {self.elephant:.1f}%"

    def __str__(self):
        return f"ПчёлоСлон: {self.get_percentages()}"


def main():
    """Интерактивная программа для создания ПчёлоСлона"""
    print("=== СОЗДАНИЕ ПЧЁЛОСЛОНА ===")

    try:
        bee = int(input("Введите часть пчелы (целое число): "))
        elephant = int(input("Введите часть слона (целое число): "))

        be = BeeElephant(bee, elephant)

        while True:
            print(f"\n{be}")
            print(f"Текущий звук: {be.trumpet()}")
            print(f"Может летать: {be.fly()}")

            print("\nВыберите действие:")
            print("1. Покормить нектаром")
            print("2. Покормить травой")
            print("3. Создать нового ПчёлоСлона")
            print("4. Выйти")

            choice = input("Ваш выбор (1-4): ")

            if choice == '1':
                try:
                    value = int(input("Сколько нектара дать? "))
                    be.eat("nectar", value)
                    print(f"Покормлен нектаром! Новый звук: {be.trumpet()}")
                except ValueError:
                    print("Ошибка: введите число!")

            elif choice == '2':
                try:
                    value = int(input("Сколько травы дать? "))
                    be.eat("grass", value)
                    print(f"Покормлен травой! Новый звук: {be.trumpet()}")
                except ValueError:
                    print("Ошибка: введите число!")

            elif choice == '3':
                bee = int(input("Введите часть пчелы (целое число): "))
                elephant = int(input("Введите часть слона (целое число): "))
                be = BeeElephant(bee, elephant)

            elif choice == '4':
                print("До свидания!")
                break

            else:
                print("Неверный выбор!")

    except ValueError:
        print("Ошибка: введите целые числа!")


# Демонстрация работы
if __name__ == "__main__":
    print("=== ДЕМОНСТРАЦИЯ РАБОТЫ ПЧЁЛОСЛОНА ===")

    # Тестовые примеры согласно требованиям (точные значения)
    test_cases = [
        (100, 0),  # 100% пчела
        (75, 25),  # 75% пчела
        (50, 50),  # 50/50
        (25, 75),  # 25% пчела
        (0, 100),  # 100% слон
    ]

    print("=== ТОЧНЫЕ КРИТИЧЕСКИЕ ТОЧКИ ===")
    for bee, elephant in test_cases:
        be = BeeElephant(bee, elephant)
        print(f"\n{bee}/{elephant}: {be.get_percentages()}")
        print(f"Звук: {be.trumpet()}")
        print(f"Может летать: {be.fly()}")

    print("\n=== ПРОМЕЖУТОЧНЫЕ ЗНАЧЕНИЯ ===")
    # Промежуточные значения для демонстрации
    intermediate_cases = [
        (90, 10),  # ближе к 100% пчела
        (80, 20),  # ближе к 75% пчела
        (60, 40),  # ближе к 50/50
        (40, 60),  # ближе к 50/50
        (30, 70),  # ближе к 25% пчела
        (10, 90),  # ближе к 0% пчела
    ]

    for bee, elephant in intermediate_cases:
        be = BeeElephant(bee, elephant)
        print(f"\n{bee}/{elephant}: {be.get_percentages()}")
        print(f"Звук: {be.trumpet()}")
        print(f"Может летать: {be.fly()}")

    # Запуск интерактивной программы
    main()