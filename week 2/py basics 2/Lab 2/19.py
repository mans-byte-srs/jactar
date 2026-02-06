n = int(input())
episodes = {}
for _ in range(n):
    line = input().split()
    name = line[0]
    count = int(line[1])
    if name in episodes:
        episodes[name] += count
    else:
        episodes[name] = count
for dorama in sorted(episodes):
    print(dorama, episodes[dorama])