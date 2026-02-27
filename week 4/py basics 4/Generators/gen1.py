def count_up(n):

    for i in range(1, n + 1):
        yield i 
n = int(input())
# Звездочка * распаковывает все числа из генератора в одну строку через пробел
print(*(count_up(n)))