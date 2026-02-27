def outer():
    count = 5
    def inner():
        nonlocal count
        count += 1
    inner()
    return count
print(outer()) # 6