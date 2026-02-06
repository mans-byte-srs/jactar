from collections import Counter

n = int(input())
numbers = [input().strip() for _ in range(n)]
count = Counter(numbers)
result = sum(1 for freq in count.values() if freq == 3)
print(result)