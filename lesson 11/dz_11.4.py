import math


class Sphere:
    def __init__(self, radius=1, x=0, y=0, z=0):
        """
        Конструктор сферы
        - без аргументов: радиус=1, центр=(0,0,0)
        - только радиус: заданный радиус, центр=(0,0,0)
        - все параметры: заданные радиус и центр
        """
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z

    def get_volume(self):
        """Объем шара: V = (4/3) * π * r³"""
        return (4 / 3) * math.pi * (self.radius ** 3)

    def get_square(self):
        """Площадь поверхности: S = 4 * π * r²"""
        return 4 * math.pi * (self.radius ** 2)

    def get_radius(self):
        """Возвращает радиус сферы"""
        return self.radius

    def get_center(self):
        """Возвращает кортеж с координатами центра"""
        return (self.x, self.y, self.z)

    def set_radius(self, radius):
        """Устанавливает новый радиус"""
        self.radius = radius

    def set_center(self, x, y, z):
        """Устанавливает новые координаты центра"""
        self.x = x
        self.y = y
        self.z = z

    def is_point_inside(self, x, y, z):
        """
        Проверяет, находится ли точка внутри сферы
        Расстояние от центра до точки должно быть <= радиусу
        """
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2 + (z - self.z) ** 2)
        return distance <= self.radius

    def __str__(self):
        """Строковое представление сферы"""
        return f"Сфера: радиус={self.radius}, центр=({self.x}, {self.y}, {self.z})"


# Примеры использования
print("=== Различные способы создания сфер ===")
sphere1 = Sphere()  # радиус=1, центр=(0,0,0)
print(sphere1)
print(f"Объем: {sphere1.get_volume():.2f}")
print(f"Площадь: {sphere1.get_square():.2f}")

sphere2 = Sphere(3)  # радиус=3, центр=(0,0,0)
print(f"\n{sphere2}")
print(f"Объем: {sphere2.get_volume():.2f}")

sphere3 = Sphere(2, 1, 2, 3)  # радиус=2, центр=(1,2,3)
print(f"\n{sphere3}")

print("\n=== Проверка точек ===")
print(f"Точка (0,0,0) внутри sphere1: {sphere1.is_point_inside(0, 0, 0)}")
print(f"Точка (2,0,0) внутри sphere1: {sphere1.is_point_inside(2, 0, 0)}")
print(f"Точка (1,2,3) внутри sphere3: {sphere3.is_point_inside(1, 2, 3)}")
print(f"Точка (4,2,3) внутри sphere3: {sphere3.is_point_inside(4, 2, 3)}")

print("\n=== Изменение параметров ===")
sphere1.set_radius(5)
sphere1.set_center(10, 20, 30)
print(f"После изменений: {sphere1}")
print(f"Новый центр: {sphere1.get_center()}")
print(f"Новый радиус: {sphere1.get_radius()}")