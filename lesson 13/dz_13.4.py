from abc import ABC, abstractmethod


# Абстрактный класс Animal
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass


# Конкретные классы животных
class Dog(Animal):
    def speak(self):
        return "Гав-гав!"


class Cat(Animal):
    def speak(self):
        return "Мяу-мяу!"


# Фабрика животных
class AnimalFactory:
    def create_animal(self, animal_type):
        animal_type = animal_type.lower()

        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            raise ValueError(f"Неизвестный тип животного: {animal_type}")


def main():
    """Основная функция программы"""
    factory = AnimalFactory()

    print("=== ФАБРИКА ЖИВОТНЫХ ===")

    while True:
        print("\nВыберите действие:")
        print("1. Создать собаку")
        print("2. Создать кошку")
        print("3. Выйти")

        choice = input("Ваш выбор (1-3): ")

        if choice == '1':
            animal = factory.create_animal("dog")
            print(f"Создана собака! Она говорит: {animal.speak()}")

        elif choice == '2':
            animal = factory.create_animal("cat")
            print(f"Создана кошка! Она говорит: {animal.speak()}")

        elif choice == '3':
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор!")


# Дополнительная функция для демонстрации работы с вводом от пользователя
def create_custom_animal():
    """Создание животного по вводу пользователя"""
    factory = AnimalFactory()

    print("\n=== СОЗДАНИЕ ЖИВОТНОГО ===")

    while True:
        animal_type = input("Введите тип животного (dog/cat) или 'exit' для выхода: ").strip().lower()

        if animal_type == 'exit':
            break

        try:
            animal = factory.create_animal(animal_type)
            print(f"✅ Создано животное! Оно говорит: {animal.speak()}")
        except ValueError as e:
            print(f"❌ Ошибка: {e}")


# Запуск программы
if __name__ == "__main__":
    # Основное меню
    while True:
        print("\n" + "=" * 40)
        print("ПАТТЕРН 'ФАБРИЧНЫЙ МЕТОД'")
        print("=" * 40)
        print("1. Простое меню")
        print("2. Создание по вводу")
        print("3. Выйти")
        print("=" * 40)

        choice = input("Выберите режим (1-3): ")

        if choice == '1':
            main()
        elif choice == '2':
            create_custom_animal()
        elif choice == '3':
            print("До свидания!")
            break
        else:
            print("Неверный выбор!")