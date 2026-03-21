# Чтение всего файла целиком
with open("test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print("Весь файл:", content)

# Чтение построчно
with open("test.txt", "r", encoding="utf-8") as f:
    for line in f:
        print("Строка:", line.strip())