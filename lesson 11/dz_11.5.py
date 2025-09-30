class SuperStr(str):
    def is_repeatance(self, s):
        """
        Проверяет, может ли текущая строка быть получена 
        целым количеством повторов строки s
        """
        if not s or not self:  # пустая строка s или пустая текущая строка
            return False

        # Если длина текущей строки не делится на длину s без остатка,
        # то повторением быть не может
        if len(self) % len(s) != 0:
            return False

        # Проверяем, состоит ли строка из повторений s
        repeat_count = len(self) // len(s)
        return self == s * repeat_count

    def is_palindrom(self):
        """
        Проверяет, является ли строка палиндромом
        (игнорирует регистр)
        """
        # Приводим к нижнему регистру и убираем пробелы для более строгой проверки
        clean_str = self.lower().replace(" ", "")
        return clean_str == clean_str[::-1]


# Примеры использования
print("=== Проверка повторений ===")
s1 = SuperStr("abcabcabc")
print(f"'{s1}'.is_repeatance('abc') = {s1.is_repeatance('abc')}")
print(f"'{s1}'.is_repeatance('ab') = {s1.is_repeatance('ab')}")
print(f"'{s1}'.is_repeatance('abcabc') = {s1.is_repeatance('abcabc')}")

s2 = SuperStr("aaaa")
print(f"'{s2}'.is_repeatance('a') = {s2.is_repeatance('a')}")
print(f"'{s2}'.is_repeatance('aa') = {s2.is_repeatance('aa')}")

s3 = SuperStr("")
print(f"''.is_repeatance('a') = {s3.is_repeatance('a')}")

print("\n=== Проверка палиндромов ===")
p1 = SuperStr("radar")
print(f"'{p1}'.is_palindrom() = {p1.is_palindrom()}")

p2 = SuperStr("A man a plan a canal Panama")
print(f"'{p2}'.is_palindrom() = {p2.is_palindrom()}")

p3 = SuperStr("Hello")
print(f"'{p3}'.is_palindrom() = {p3.is_palindrom()}")

p4 = SuperStr("")
print(f"''.is_palindrom() = {p4.is_palindrom()}")

p5 = SuperStr("Madam")
print(f"'{p5}'.is_palindrom() = {p5.is_palindrom()}")

# Демонстрация наследования от str
print("\n=== Наследование от str ===")
s = SuperStr("Test String")
print(f"Длина: {len(s)}")
print(f"Верхний регистр: {s.upper()}")
print(f"Замена: {s.replace('Test', 'Super')}")
