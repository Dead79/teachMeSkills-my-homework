class Soda:
    def __init__(self, taste=None):
        # Список допустимых вкусов
        self.valid_tastes = ["кола", "фанта", "спрайт", "тоник"]

        if taste and taste in self.valid_tastes:
            self.taste = taste
        else:
            self.taste = None

    def __str__(self):
        if self.taste:
            return f"У вас газировка с вкусом {self.taste}"
        else:
            return "У вас обычная газировка"


# Создаем газировку с выбором вкуса
print("Доступные вкусы: кола, фанта, спрайт, тоник")
user_taste = input("Введите вкус газировки (или нажмите Enter для обычной): ").strip().lower()

soda = Soda(user_taste)
print(soda)