import shutil
import os

# Перемещаем файл в созданную папку
# Сначала создадим пустой файл для теста
open("move_me.txt", "w").close()

shutil.move("move_me.txt", "new_folder/moved.txt")
print("Файл перемещен в 'new_folder'")