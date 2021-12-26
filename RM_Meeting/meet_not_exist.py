from datetime import datetime, date, timedelta

from DbReadTest import *
from unicko_api import *

ret = RTG_DB.get_cource_with_unicoID()
n = 0
for i in ret:
    if 'id' not in vUnicko.get_specific_meeting(i[0]):
        n += 1
        print(i,n)
print(len(ret))