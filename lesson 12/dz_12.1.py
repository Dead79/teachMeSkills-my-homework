import os

class Product:
    def __init__(self, name, store, price):
        self.__name = name
        self.__store = store
        self.__price = price

    # Геттеры
    def get_name(self):
        return self.__name

    def get_store(self):
        return self.__store

    def get_price(self):
        return self.__price

    # Сеттеры
    def set_name(self, name):
        self.__name = name

    def set_store(self, store):
        self.__store = store

    def set_price(self, price):
        self.__price = price

    def __str__(self):
        return f"Товар: {self.__name}, Магазин: {self.__store}, Цена: {self.__price} руб."

    def to_file_string(self):
        """Преобразует товар в строку для записи в файл"""
        return f"{self.__name}|{self.__store}|{self.__price}"

    def __add__(self, other):
        """Перегрузка сложения: сумма цен товаров"""
        if isinstance(other, Product):
            return self.__price + other.__price
        elif isinstance(other, (int, float)):
            return self.__price + other
        else:
            raise TypeError("Можно складывать только с товаром или числом")

    def __radd__(self, other):
        """Правое сложение"""
        return self.__add__(other)


class Warehouse:
    def __init__(self, filename="products.txt"):
        self.__products = []
        self.filename = filename
        self.load_from_file()

    def load_from_file(self):
        """Загружает товары из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line:
                            parts = line.split('|')
                            if len(parts) == 3:
                                name, store, price = parts
                                product = Product(name, store, float(price))
                                self.__products.append(product)
                print(f"Данные загружены из файла {self.filename}")
            except Exception as e:
                print(f"Ошибка при загрузке файла: {e}")

    def save_to_file(self):
        """Сохраняет товары в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                for product in self.__products:
                    file.write(product.to_file_string() + '\n')
            print(f"Данные сохранены в файл {self.filename}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def add_product(self, product):
        """Добавление товара на склад"""
        if isinstance(product, Product):
            self.__products.append(product)
            self.save_to_file()
            print("Товар добавлен и сохранен в файл")
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    def remove_product(self, index):
        """Удаление товара по индексу"""
        if 0 <= index < len(self.__products):
            removed_product = self.__products.pop(index)
            self.save_to_file()
            print(f"Товар '{removed_product.get_name()}' удален")
        else:
            raise IndexError("Товара с таким индексом не существует")

    def update_product(self, index, name=None, store=None, price=None):
        """Обновление информации о товаре"""
        if 0 <= index < len(self.__products):
            product = self.__products[index]
            if name:
                product.set_name(name)
            if store:
                product.set_store(store)
            if price:
                product.set_price(float(price))
            self.save_to_file()
            print(f"Товар обновлен: {product}")
        else:
            raise IndexError("Товара с таким индексом не существует")

    def get_product_by_index(self, index):
        """Вывод информации о товаре по индексу"""
        if 0 <= index < len(self.__products):
            return self.__products[index]
        else:
            raise IndexError("Товара с таким индексом не существует")

    def get_product_by_name(self, name):
        """Вывод информации о товаре по имени"""
        for product in self.__products:
            if product.get_name().lower() == name.lower():
                return product
        return None

    def sort_by_name(self):
        """Сортировка товаров по названию"""
        self.__products.sort(key=lambda x: x.get_name())
        self.save_to_file()

    def sort_by_store(self):
        """Сортировка товаров по названию магазина"""
        self.__products.sort(key=lambda x: x.get_store())
        self.save_to_file()

    def sort_by_price(self):
        """Сортировка товаров по цене"""
        self.__products.sort(key=lambda x: x.get_price())
        self.save_to_file()

    def display_all_products(self):
        """Вывод всех товаров на складе"""
        if not self.__products:
            print("Склад пуст")
            return

        print("\n=== ТОВАРЫ НА СКЛАДЕ ===")
        for i, product in enumerate(self.__products):
            print(f"{i}: {product}")

    def get_total_value(self):
        """Общая стоимость всех товаров"""
        return sum(product.get_price() for product in self.__products)

    def __len__(self):
        """Количество товаров на складе"""
        return len(self.__products)


def main_menu():
    """Главное меню программы"""
    warehouse = Warehouse()

    while True:
        print("\n" + "=" * 50)
        print("СИСТЕМА УПРАВЛЕНИЯ СКЛАДОМ")
        print("=" * 50)
        print("1. Показать все товары")
        print("2. Добавить товар")
        print("3. Удалить товар")
        print("4. Редактировать товар")
        print("5. Найти товар по имени")
        print("6. Найти товар по индексу")
        print("7. Сортировать товары")
        print("8. Общая стоимость товаров")
        print("9. Сохранить в файл")
        print("0. Выход")
        print("=" * 50)

        choice = input("Выберите действие (0-9): ")

        if choice == '1':
            warehouse.display_all_products()

        elif choice == '2':
            print("\nДОБАВЛЕНИЕ ТОВАРА:")
            name = input("Название товара: ")
            store = input("Название магазина: ")
            try:
                price = float(input("Цена: "))
                product = Product(name, store, price)
                warehouse.add_product(product)
            except ValueError:
                print("Ошибка: цена должна быть числом!")

        elif choice == '3':
            warehouse.display_all_products()
            if len(warehouse) > 0:
                try:
                    index = int(input("\nВведите индекс товара для удаления: "))
                    warehouse.remove_product(index)
                except (ValueError, IndexError) as e:
                    print(f"Ошибка: {e}")

        elif choice == '4':
            warehouse.display_all_products()
            if len(warehouse) > 0:
                try:
                    index = int(input("\nВведите индекс товара для редактирования: "))
                    print("Введите новые данные (оставьте пустым чтобы не менять):")
                    name = input("Новое название: ") or None
                    store = input("Новый магазин: ") or None
                    price_str = input("Новая цена: ")
                    price = float(price_str) if price_str else None
                    warehouse.update_product(index, name, store, price)
                except (ValueError, IndexError) as e:
                    print(f"Ошибка: {e}")

        elif choice == '5':
            name = input("Введите название товара для поиска: ")
            product = warehouse.get_product_by_name(name)
            if product:
                print(f"Найден товар: {product}")
            else:
                print("Товар не найден")

        elif choice == '6':
            try:
                index = int(input("Введите индекс товара: "))
                product = warehouse.get_product_by_index(index)
                print(f"Товар: {product}")
            except (ValueError, IndexError) as e:
                print(f"Ошибка: {e}")

        elif choice == '7':
            print("\nСОРТИРОВКА:")
            print("1. По названию")
            print("2. По магазину")
            print("3. По цене")
            sort_choice = input("Выберите тип сортировки (1-3): ")
            if sort_choice == '1':
                warehouse.sort_by_name()
                print("Товары отсортированы по названию")
            elif sort_choice == '2':
                warehouse.sort_by_store()
                print("Товары отсортированы по магазину")
            elif sort_choice == '3':
                warehouse.sort_by_price()
                print("Товары отсортированы по цене")

        elif choice == '8':
            total = warehouse.get_total_value()
            print(f"Общая стоимость всех товаров: {total:.2f} руб.")

        elif choice == '9':
            warehouse.save_to_file()

        elif choice == '0':
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор! Попробуйте снова.")


# Запуск программы
if __name__ == "__main__":
    main_menu()