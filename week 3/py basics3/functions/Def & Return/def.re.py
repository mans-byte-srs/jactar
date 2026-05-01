# 1. Площадь
def get_area(width, height):
    return width * height

# 2. Четность
def is_even(number):
    return number % 2 == 0

# 3. Конвертер (курс 90)
def convert_to_usd(rubles):
    return rubles / 90

#4. Вызов функции и вывод результата
def multiply_numbers(a, b):
    return a * b
result = multiply_numbers(5, 10)

print(f"Результат умножения: {result}")
print(f"Площадь: {get_area(10, 5)}")
print(f"Число 7 четное? {is_even(7)}")
print(f"18000 руб в USD: ${convert_to_usd(18000)}")