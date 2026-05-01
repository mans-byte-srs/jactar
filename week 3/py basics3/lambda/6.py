a=int(input())
b=list(map(int, input().split()))
s=max(b)
f=min(b)
for i in range(a):
    if(b[i]==s):
       print(f, end=" ")
    else:
        print (b[i], end=" ")
        