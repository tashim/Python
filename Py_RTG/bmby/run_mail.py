import os
import subprocess
import socket
from time import sleep

from apscheduler.triggers import cron
from apscheduler.schedulers.background import BackgroundScheduler

from test import log


def internet(host="8.8.8.8", port=53, timeout=3):
  """
  Host: 8.8.8.8 (google-public-dns-a.google.com)
  OpenPort: 53/tcp
  Service: domain (DNS/TCP)
  """
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except Exception as ex:
    # print(ex)
    return False
is_run = 0
def run():
    global is_run
    is_run = 1
    print("run 2 wait")
    os.chdir('./run12')
    for dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith(".exe")]:
            while not internet():                    pass
            log("run "+str(filename))
            subprocess.call(os.path.join(dirpath, filename))
            # os.startfile("Soap1.exe")
    os.chdir('./../')
    is_run = 0

def run_2():
    if is_run == 1: return
    os.chdir('./run')
    for  dirpath, dirnames, filenames in os.walk("."):
        for filename in [f for f in filenames if f.endswith(".exe")]:
            try:
                while not internet():                    pass
                ret = os.startfile(os.path.join(dirpath, filename))
            except:
                pass
    os.chdir('./../')
    print("run 2 out")

scheduler = BackgroundScheduler()
scheduler.start()

trigger = cron.CronTrigger(hour='22', minute=0, second=30)
scheduler.add_job(run, trigger=trigger)

trigger = cron.CronTrigger( minute='*/3')
scheduler.add_job(run_2, trigger=trigger)
while 1:
    sleep(10000)
    pass