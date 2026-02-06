n = int(input())
nums = input().split()

min = int(nums[0])
ind=0

for i in range(n):
    if min<int(nums[i]):
        min = int(nums[i])
        ind= i
print(ind+1)
