import os
import shutil

# Копируем файл
shutil.copy("output.txt", "copy_output.txt")
print("Файл скопирован")

# Удаляем файл (будь осторожен!)
if os.path.exists("copy_output.txt"):
    os.remove("copy_output.txt")
    print("Файл удален")