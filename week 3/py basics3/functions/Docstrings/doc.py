def find_max(numbers):
    """Принимает список чисел и возвращает самое большое из них."""
    if not numbers: return None
    return max(numbers)

def filter_short_names(names, min_length):
    """
    Возвращает новый список имен, длина которых больше min_length.
    """
    return [name for name in names if len(name) > min_length]

def scale_values(data, factor):
    """Умножает каждый элемент списка data на число factor."""
    return [x * factor for x in data]

# Тесты
my_nums = [1, 45, 12, 8]
print(f"Максимум: {find_max(my_nums)}")
print(f"Длинные имена: {filter_short_names(['Ян', 'Александр', 'Ли'], 3)}")
print(f"Масштабирование: {scale_values([1, 2, 3], 10)}")