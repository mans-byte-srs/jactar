n = int(input())
numbers = list(map(int, input().split()))

# set() арқылы қайталанатын сандарды өшіріп, sorted() арқылы реттейміз
unique_sorted = sorted(set(numbers))

# Тізімдегі сандарды бос орын арқылы шығару
print(*(unique_sorted))