n = int(input())
nums = input().split()

total = int(nums[0])

for i in range(n):
    if total<int(nums[i]):
        total = int(nums[i])
print(total)
