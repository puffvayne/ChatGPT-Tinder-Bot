import pytz
from tzlocal import get_localzone
import datetime


local_tz = get_localzone()
local_now = datetime.datetime.now(tz=local_tz)

target_tz = pytz.timezone('Asia/Taipei')
target_now = datetime.datetime.now(tz=target_tz)

# Calculate hour difference
server_offset = local_now.astimezone(local_tz).utcoffset()
target_offset = target_now.astimezone(target_tz).utcoffset()

hour_diff = (target_offset - server_offset).total_seconds() / 3600

print("Hour difference:", hour_diff)
