n = int(input())
arr = [input().strip() for _ in range(n)]

# Словарь: ключ = слово, значение = индекс первого появления (с 1)
first_index = {}
for i, word in enumerate(arr):
    if word not in first_index:
        first_index[word] = i + 1 

# Выводим слова в лексикографическом порядке с их первым индексом
for word in sorted(first_index):
    print(word, first_index[word])