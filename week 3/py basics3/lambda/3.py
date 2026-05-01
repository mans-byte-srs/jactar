a=int(input())
b=list(map(int, input().split()))
s=0
for i in range(a):
    if(b[i]>0):
        s+=1
print(s)