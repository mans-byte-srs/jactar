n = int(input())
numbers = list(map(int, input().split()))

# Барлық сан 0-ден үлкен немесе тең екенін тексереміз
if all(x >= 0 for x in numbers):
    print("Yes")
else:
    print("No")