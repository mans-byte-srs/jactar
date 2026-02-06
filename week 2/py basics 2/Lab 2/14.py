from collections import Counter

# Вводим n
n = int(input())

# Вводим список чисел
nums = list(map(int, input().split()))

# Считаем частоту каждого числа
count = Counter(nums)

# Находим максимальную частоту
max_freq = max(count.values())

# Берём все числа с этой частотой
candidates = [num for num, freq in count.items() if freq == max_freq]

# Выводим минимальное среди них
print(min(candidates))