class Car:
    def __init__(self, color, type, year):
        self.color = color
        self.type = type
        self.year = year
        self.is_running = False  # дополнительный атрибут для отслеживания состояния

    def start(self):
        """Запуск автомобиля"""
        if not self.is_running:
            self.is_running = True
            print("Автомобиль заведён")
        else:
            print("Автомобиль уже заведён")

    def stop(self):
        """Отключение автомобиля"""
        if self.is_running:
            self.is_running = False
            print("Автомобиль заглушен")
        else:
            print("Автомобиль уже заглушен")

    def set_color(self, new_color):
        """Установка нового цвета"""
        self.color = new_color
        print(f"Цвет автомобиля изменён на {new_color}")

    def set_type(self, new_type):
        """Установка нового типа"""
        self.type = new_type
        print(f"Тип автомобиля изменён на {new_type}")

    def set_year(self, new_year):
        """Установка нового года выпуска"""
        self.year = new_year
        print(f"Год выпуска автомобиля изменён на {new_year}")

    def __str__(self):
        """Строковое представление автомобиля"""
        status = "заведён" if self.is_running else "заглушен"
        return f"Автомобиль: {self.color} {self.type} {self.year} года ({status})"


# Пример использования
car1 = Car("красный", "седан", 2020)
print(car1)

car1.start()
car1.set_color("синий")
car1.set_year(2022)
car1.stop()

print(car1)