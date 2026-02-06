n = int(input())
nums = input().split()

total = 0
for i in range(n):
    if (int(nums[i]))>0:
        total+=1
print(total)