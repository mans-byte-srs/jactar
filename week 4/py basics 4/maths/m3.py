import importlib
try:
    importlib.import_module('invalid_name')
except ModuleNotFoundError:
    print("Модуль не найден")