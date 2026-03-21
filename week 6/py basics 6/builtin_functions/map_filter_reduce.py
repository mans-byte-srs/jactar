from functools import reduce

nums = [1, 2, 3, 4, 5]

# map: возводим в квадрат
squares = list(map(lambda x: x**2, nums)) # [1, 4, 9, 16, 25]

# filter: только числа больше 2
filtered = list(filter(lambda x: x > 2, nums)) # [3, 4, 5]

# reduce: перемножаем все числа
product = reduce(lambda x, y: x * y, nums) # 120

print(f"Squares: {squares}\nFiltered: {filtered}\nProduct: {product}")