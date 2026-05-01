n = int(input())
numbers = map(int, input().split())

# Әр санды bool түріне айналдырып, олардың қосындысын табамыз
truthy_count = sum(map(bool, numbers))

print(truthy_count)