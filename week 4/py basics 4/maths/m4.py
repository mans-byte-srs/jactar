import math
# Выводит все имена в модуле, которые не начинаются с подчеркивания
print([name for name in dir(math) if not name.startswith('_')][:5])