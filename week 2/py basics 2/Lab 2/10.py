a=int(input())
nums = input().split()
nums = [int(x) for x in nums]
nums.sort(reverse=True)
for x in nums:
    print(x, end=' ')