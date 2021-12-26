import os

import os.path
import webbrowser
from datetime import date, timedelta, datetime

from apscheduler.triggers import interval, cron

from DB import get_user
from test import log


def files():
    for dirpath, dirnames, filenames in os.walk("./run"):
        print(os.path.basename(__file__))
        print(dirnames)
        # for filename in filenames:
        for filename in \
                [
                    f for f in filenames #if (f.endswith(".exe")
                        # and os.path.basename(__file__).split('.')[0] != f.split('.')[0])
                ]:
            print("os", os.path.join(dirpath, filename))
            print("path",dirpath)
            print("name",dirnames)

        print(dirpath)

# os.system("cmd")
import sched, time

def action():
    print("a1=",datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

def action2():
    print("a2",datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

# today = date.today() - timedelta(days=-1)
# t = today.timetuple()
# # Set up scheduler
# # s = sched.scheduler(time.localtime, time.sleep)
# s = sched.scheduler(time.time, time.sleep)
# print(t.tm_mday)
# t = datetime.now()
#
# s.enterabs(t.time(), 0, action,())
# # s.enter(2, 0, action,())
# # s.enter(5, 0, action,())
# # Block until the action has been run
# s.run()
# log("kdkdkk")
log("test2")
s = 'f'
print(type(str()))
print(type(s))
if type(s) is type(str()):
 print('y')
else:
 print('n')