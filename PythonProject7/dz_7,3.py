def palindrome(s):
    return s == s[::-1]

strings = input("Введите слова через пробел: ").split()
palindromes = list(filter(palindrome, strings))

print("Все строки:", strings)
print("Палиндромы:", palindromes)