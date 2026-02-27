from datetime import datetime
s = "2026-12-31"
dt = datetime.strptime(s, "%Y-%m-%d")
print(dt.year)