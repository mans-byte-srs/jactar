import os

# Создаем новую папку
if not os.path.exists("new_folder"):
    os.mkdir("new_folder")

# Выводим список всех файлов и папок в текущей директории
items = os.listdir(".")
print("Содержимое папки:", items)