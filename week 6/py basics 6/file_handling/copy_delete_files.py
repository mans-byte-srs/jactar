import os
import shutil

shutil.copy("output.txt", "copy_output.txt")
print("Файл скопирован")

if os.path.exists("copy_output.txt"):
    os.remove("copy_output.txt")
    print("Файл удален")