n = int(input())
arr = list(map(int, input().split()))

seen = set() 

for x in arr:
    if x in seen:
        print("NO")
    else:
        print("YES")
        seen.add(x) 