a = int(input())

if a > 0 and (a & (a - 1)) == 0:
    print("YES")
else:
    print("NO")