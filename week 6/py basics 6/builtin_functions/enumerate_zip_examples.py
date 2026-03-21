names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 95]

# enumerate: получаем индекс и значение
for i, name in enumerate(names, 1):
    print(f"{i}. {name}")

# zip: объединяем два списка
for name, score in zip(names, scores):
    print(f"User {name} has score {score}")

# Type conversion
num_str = "100"
num_int = int(num_str)
print(f"Type of {num_int} is {type(num_int)}")