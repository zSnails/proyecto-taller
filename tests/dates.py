from datetime import datetime, timedelta, time

time1 = timedelta(hours=3, minutes=1, seconds=5)
time2 = timedelta(hours=2, minutes=10, seconds=5)

print((time1 - time2).total_seconds())

# time3 = time(hour = 3, minute=1, second=5)
# time4 = time(hour=3, minute=10, second=4)

# print((time3 - time4).total_seconds())

time3 = time.fromisoformat("3:1:5")
time4 = time.fromisoformat("2:10:5")

print((time3 - time4).total_seconds())
