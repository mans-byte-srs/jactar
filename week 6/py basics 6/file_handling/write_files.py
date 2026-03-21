# 'w' - перезаписывает файл
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Привет, мир!\n")

# 'a' - добавляет в конец (append)
with open("output.txt", "a", encoding="utf-8") as f:
    f.write("Добавляем новую строку.\n")