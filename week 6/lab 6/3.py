n = int(input())
words = input().split()

# enumerate арқылы индекс пен сөзді жұп қылып аламыз
pairs = [f"{i}:{word}" for i, word in enumerate(words)]

# Барлығын бір жолға бос орын арқылы шығарамыз
print(" ".join(pairs))