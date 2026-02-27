import math
name = input() # Введи 'pi' или 'sin'
obj = getattr(math, name)
print("Это функция" if callable(obj) else "Это число")