s = input().lower()
vowels = "aeiou"

# any() арқылы әрбір әріптің дауысты екенін тексереміз
if any(char in vowels for char in s):
    print("Yes")
else:
    print("No")