from pytz import timezone
import datetime

tw_tz = timezone('Asia/Taipei')
x = datetime.datetime.now(tz=tw_tz)
print(x)
y = datetime.datetime.now()
print(y)

import os, time, datetime

os.environ['TZ'] = 'Asia/Taipei'
time.tzset()
print(datetime.datetime.now())
