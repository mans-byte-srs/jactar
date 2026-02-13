# 1. Определение и вызов
def multiply(a, b):
    """Возвращает произведение двух чисел."""
    return a * b

# 2. Аргументы: позиционные и по умолчанию 
def create_profile(username, city="Не указан"):
    print(f"Пользователь: {username}, Город: {city}")

# 3. Гибкие аргументы (*args, **kwargs)
def print_order(*items, **details):
    print(f"Товары: {items}")
    for key, value in details.items():
        print(f"{key}: {value}")

# 4. Передача списка 
def process_list(data):
    return [x * 2 for x in data]

print(f"Умножение: {multiply(5, 5)}")
create_profile("Ivan_99")
print_order("Хлеб", "Молоко", address="Москва", urgent=True)
print(f"Список x2: {process_list([1, 2, 3])}")