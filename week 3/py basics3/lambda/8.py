a=int(input())
s=[]
b=list(map(int, input().split()))
for i in range(a):
    if b[i] in s:
        print("notnew")
    else:
        print("new")
    if b[i] not in s:
        s.append(b[i])