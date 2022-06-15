from datetime import datetime, timedelta
dt1 = datetime(year=5, month=1, day=1, minute=30, hour=10, second=5)
dt2 = datetime(year=5, month=1, day=1, minute=31, hour=10, second=0)
dt = dt2 - dt1
q = timedelta(minutes=1)
print(dt)
print(q)
print( dt <= q )