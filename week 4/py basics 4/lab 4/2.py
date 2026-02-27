n = int(input())

first = True
for i in range(0, n + 1, 2):
    if not first:
        print(",", end="")
    print(i, end="")
    first = False