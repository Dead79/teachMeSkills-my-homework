class Pizza:
    def __init__(self):
        self.size = None
        self.cheese = False
        self.pepperoni = False
        self.mushrooms = False
        self.onions = False
        self.bacon = False

    def __str__(self):
        ingredients = []
        if self.cheese:
            ingredients.append("сыр")
        if self.pepperoni:
            ingredients.append("пепперони")
        if self.mushrooms:
            ingredients.append("грибы")
        if self.onions:
            ingredients.append("лук")
        if self.bacon:
            ingredients.append("бекон")

        ingredients_str = ", ".join(ingredients) if ingredients else "нет ингредиентов"
        return f"Пицца {self.size} см с: {ingredients_str}"


class PizzaBuilder:
    def __init__(self):
        self.pizza = Pizza()

    def set_size(self, size):
        self.pizza.size = size
        return self

    def add_cheese(self):
        self.pizza.cheese = True
        return self

    def add_pepperoni(self):
        self.pizza.pepperoni = True
        return self

    def add_mushrooms(self):
        self.pizza.mushrooms = True
        return self

    def add_onions(self):
        self.pizza.onions = True
        return self

    def add_bacon(self):
        self.pizza.bacon = True
        return self

    def build(self):
        return self.pizza


class PizzaDirector:
    def __init__(self, builder):
        self.builder = builder

    def make_pizza(self, size, ingredients):
        """Создает пиццу с заданным размером и ингредиентами"""
        self.builder.set_size(size)

        if "cheese" in ingredients:
            self.builder.add_cheese()
        if "pepperoni" in ingredients:
            self.builder.add_pepperoni()
        if "mushrooms" in ingredients:
            self.builder.add_mushrooms()
        if "onions" in ingredients:
            self.builder.add_onions()
        if "bacon" in ingredients:
            self.builder.add_bacon()

        return self.builder.build()


def main():
    """Основная функция для демонстрации работы"""
    print("=== ПАТТЕРН 'СТРОИТЕЛЬ' ДЛЯ ПИЦЦЫ ===")

    while True:
        print("\nВыберите способ создания пиццы:")
        print("1. Создать пиццу вручную (через Builder)")
        print("2. Создать пиццу через Director")
        print("3. Выйти")

        choice = input("Ваш выбор (1-3): ")

        if choice == '1':
            create_pizza_manually()
        elif choice == '2':
            create_pizza_with_director()
        elif choice == '3':
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор!")


def create_pizza_manually():
    """Создание пиццы вручную через Builder"""
    print("\n=== СОЗДАНИЕ ПИЦЦЫ ВРУЧНУЮ ===")

    builder = PizzaBuilder()

    try:
        size = int(input("Введите размер пиццы (см): "))
        builder.set_size(size)

        print("\nДобавьте ингредиенты (введите цифры через пробел):")
        print("1. Сыр")
        print("2. Пепперони")
        print("3. Грибы")
        print("4. Лук")
        print("5. Бекон")

        ingredients_choice = input("Ваш выбор: ").split()

        for choice in ingredients_choice:
            if choice == '1':
                builder.add_cheese()
            elif choice == '2':
                builder.add_pepperoni()
            elif choice == '3':
                builder.add_mushrooms()
            elif choice == '4':
                builder.add_onions()
            elif choice == '5':
                builder.add_bacon()

        pizza = builder.build()
        print(f"\n✅ Создана: {pizza}")

    except ValueError:
        print("Ошибка: введите корректные данные!")


def create_pizza_with_director():
    """Создание пиццы через Director"""
    print("\n=== СОЗДАНИЕ ПИЦЦЫ ЧЕРЕЗ DIRECTOR ===")

    builder = PizzaBuilder()
    director = PizzaDirector(builder)

    try:
        size = int(input("Введите размер пиццы (см): "))

        print("\nВыберите ингредиенты (введите названия через пробел):")
        print("Доступные: cheese, pepperoni, mushrooms, onions, bacon")

        ingredients_input = input("Ваш выбор: ").lower().split()

        pizza = director.make_pizza(size, ingredients_input)
        print(f"\n✅ Создана: {pizza}")

    except ValueError:
        print("Ошибка: введите корректные данные!")


# Запуск программы
if __name__ == "__main__":
    main()