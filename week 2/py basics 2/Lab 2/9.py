a=int(input())
jjk=input().split()
max1=int(jjk[0])
min1=int(jjk[0])
for i in range(a):
    if max1 < int(jjk[i]):
        max1=int(jjk[i])
    if min1 > int(jjk[i]):
        min1=int(jjk[i])
for i in range(a):
    num = int(jjk[i])
    if num == max1:
        print(min1, end=' ')
    else:
        print(num, end=' ')
