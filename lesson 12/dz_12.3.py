import os


class Bus:
    def __init__(self, max_seats=20, max_speed=100):
        self.speed = 0
        self.max_seats = max_seats
        self.max_speed = max_speed
        self.passengers = []  # список фамилий пассажиров
        self.has_free_seats = True
        self.seats = {}  # словарь мест: {номер_места: фамилия}
        self.filename = "avtobus.txt"

        # Инициализация мест
        for seat_num in range(1, max_seats + 1):
            self.seats[seat_num] = None

        # Загрузка данных из файла
        self.load_from_file()

    def load_from_file(self):
        """Загружает данные автобуса из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    if lines:
                        # Первая строка - скорость
                        self.speed = int(lines[0].strip())

                        # Остальные строки - пассажиры и их места
                        for line in lines[1:]:
                            line = line.strip()
                            if line and ':' in line:
                                seat_num, surname = line.split(':', 1)
                                seat_num = int(seat_num.strip())
                                surname = surname.strip()
                                if surname != "None":
                                    self.seats[seat_num] = surname
                                    self.passengers.append(surname)

                        self._update_free_seats()
                        print(f"Данные загружены из файла {self.filename}")
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")

    def save_to_file(self):
        """Сохраняет данные автобуса в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                # Сохраняем скорость
                file.write(f"{self.speed}\n")

                # Сохраняем места и пассажиров
                for seat_num, passenger in self.seats.items():
                    file.write(f"{seat_num}:{passenger if passenger else 'None'}\n")

            print(f"Данные сохранены в файл {self.filename}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def _update_free_seats(self):
        """Обновляет флаг наличия свободных мест"""
        self.has_free_seats = len(self.passengers) < self.max_seats
        self.passengers = [p for p in self.passengers if p is not None]

    def _check_movement(self):
        """Проверяет, движется ли автобус"""
        return self.speed > 0

    def board_passenger(self, surname, seat_num=None):
        """Посадка пассажира"""
        # Проверка движения автобуса
        if self._check_movement():
            print("Невозможно посадить пассажира! Автобус движется. Сначала остановите автобус.")
            return False

        if not self.has_free_seats:
            print("Нет свободных мест!")
            return False

        if surname in self.passengers:
            print(f"Пассажир {surname} уже в автобусе!")
            return False

        if seat_num:
            # Посадка на конкретное место
            if seat_num not in self.seats:
                print(f"Места {seat_num} не существует!")
                return False
            if self.seats[seat_num] is not None:
                print(f"Место {seat_num} уже занято!")
                return False
            self.seats[seat_num] = surname
        else:
            # Посадка на первое свободное место
            for seat, passenger in self.seats.items():
                if passenger is None:
                    self.seats[seat] = surname
                    seat_num = seat
                    break

        self.passengers.append(surname)
        self._update_free_seats()
        self.save_to_file()
        print(f"Пассажир {surname} сел на место {seat_num}")
        return True

    def board_multiple_passengers(self):
        """Посадка нескольких пассажиров"""
        # Проверка движения автобуса
        if self._check_movement():
            print("Невозможно посадить пассажиров! Автобус движется. Сначала остановите автобус.")
            return 0

        surnames = input("Введите фамилии пассажиров через запятую: ").split(',')
        surnames = [s.strip() for s in surnames if s.strip()]

        boarded = 0
        for surname in surnames:
            if self.board_passenger(surname):
                boarded += 1
            if not self.has_free_seats:
                print("Больше нет свободных мест!")
                break
        print(f"Посажено {boarded} пассажиров")
        return boarded

    def disembark_passenger(self, surname):
        """Высадка пассажира"""
        # Проверка движения автобуса
        if self._check_movement():
            print("Невозможно высадить пассажира! Автобус движется. Сначала остановите автобус.")
            return False

        if surname not in self.passengers:
            print(f"Пассажир {surname} не найден в автобусе!")
            return False

        # Освобождаем место
        for seat_num, passenger in self.seats.items():
            if passenger == surname:
                self.seats[seat_num] = None
                break

        self.passengers.remove(surname)
        self._update_free_seats()
        self.save_to_file()
        print(f"Пассажир {surname} вышел из автобуса")
        return True

    def disembark_multiple_passengers(self):
        """Высадка нескольких пассажиров"""
        # Проверка движения автобуса
        if self._check_movement():
            print("Невозможно высадить пассажиров! Автобус движется. Сначала остановите автобус.")
            return 0

        surnames = input("Введите фамилии пассажиров для высадки через запятую: ").split(',')
        surnames = [s.strip() for s in surnames if s.strip()]

        disembarked = 0
        for surname in surnames:
            if self.disembark_passenger(surname):
                disembarked += 1
        print(f"Высажено {disembarked} пассажиров")
        return disembarked

    def stop_bus(self):
        """Полная остановка автобуса"""
        if self.speed == 0:
            print("Автобус уже остановлен")
            return False

        self.speed = 0
        self.save_to_file()
        print("Автобус полностью остановлен")
        return True

    def change_speed(self):
        """Изменение скорости с вводом от пользователя"""
        try:
            change = int(input("На сколько изменить скорость (+/-): "))
            new_speed = self.speed + change

            if new_speed < 0:
                print("Скорость не может быть отрицательной!")
                return False
            if new_speed > self.max_speed:
                print(f"Невозможно превысить максимальную скорость {self.max_speed} км/ч!")
                return False

            self.speed = new_speed
            self.save_to_file()

            if new_speed == 0:
                print("Автобус остановлен")
            else:
                print(f"Скорость изменена до {self.speed} км/ч")
            return True
        except ValueError:
            print("Ошибка: введите число!")
            return False

    # Перегрузка операторов
    def __contains__(self, surname):
        """Оператор in: проверка наличия пассажира"""
        return surname in self.passengers

    def __iadd__(self, surname):
        """Оператор +=: посадка пассажира"""
        self.board_passenger(surname)
        return self

    def __isub__(self, surname):
        """Оператор -=: высадка пассажира"""
        self.disembark_passenger(surname)
        return self

    def __str__(self):
        """Строковое представление автобуса"""
        occupied_seats = len(self.passengers)
        free_seats = self.max_seats - occupied_seats
        status = "движется" if self.speed > 0 else "стоит"
        return (f"Автобус: скорость {self.speed} км/ч ({status}), "
                f"пассажиров: {occupied_seats}/{self.max_seats}, "
                f"свободных мест: {free_seats}")

    def show_seats(self):
        """Показать распределение мест"""
        print("\n=== РАСПРЕДЕЛЕНИЕ МЕСТ ===")
        for seat_num in range(1, self.max_seats + 1):
            passenger = self.seats[seat_num]
            status = passenger if passenger else "Свободно"
            print(f"Место {seat_num:2d}: {status}")

    def show_passengers(self):
        """Показать список пассажиров"""
        print("\n=== СПИСОК ПАССАЖИРОВ ===")
        if self.passengers:
            for i, passenger in enumerate(self.passengers, 1):
                print(f"{i}. {passenger}")
        else:
            print("Пассажиров нет")


def main_menu():
    """Главное меню программы"""
    bus = Bus()

    while True:
        print("\n" + "=" * 50)
        print("СИСТЕМА УПРАВЛЕНИЯ АВТОБУСОМ")
        print("=" * 50)
        print("1. Показать состояние автобуса")
        print("2. Показать места")
        print("3. Показать пассажиров")
        print("4. Посадить пассажира")
        print("5. Посадить нескольких пассажиров")
        print("6. Высадить пассажира")
        print("7. Высадить нескольких пассажиров")
        print("8. Изменить скорость")
        print("9. Остановить автобус")
        print("10. Проверить наличие пассажира")
        print("11. Сохранить в файл")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите действие (0-11): ")

        if choice == '1':
            print(bus)

        elif choice == '2':
            bus.show_seats()

        elif choice == '3':
            bus.show_passengers()

        elif choice == '4':
            surname = input("Введите фамилию пассажира: ").strip()
            if surname:
                seat_choice = input("Введите номер места (или Enter для любого свободного): ").strip()
                if seat_choice:
                    try:
                        seat_num = int(seat_choice)
                        bus.board_passenger(surname, seat_num)
                    except ValueError:
                        print("Ошибка: номер места должен быть числом!")
                else:
                    bus.board_passenger(surname)

        elif choice == '5':
            bus.board_multiple_passengers()

        elif choice == '6':
            surname = input("Введите фамилию пассажира для высадки: ").strip()
            if surname:
                bus.disembark_passenger(surname)

        elif choice == '7':
            bus.disembark_multiple_passengers()

        elif choice == '8':
            bus.change_speed()

        elif choice == '9':
            bus.stop_bus()

        elif choice == '10':
            surname = input("Введите фамилию для проверки: ").strip()
            if surname:
                if surname in bus:
                    print(f"Пассажир {surname} находится в автобусе")
                else:
                    print(f"Пассажир {surname} не в автобусе")

        elif choice == '11':
            bus.save_to_file()

        elif choice == '0':
            print("Выход из программы...")
            bus.save_to_file()
            break

        else:
            print("Неверный выбор! Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    main_menu()