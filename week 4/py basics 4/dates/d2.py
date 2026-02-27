from datetime import datetime, timedelta
now = datetime.now()
future = now + timedelta(days=7)
print(future.strftime("%d-%m-%Y"))