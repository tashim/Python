import subprocess
import socket

from time import  sleep


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

while 1:
    print('run')
    while not internet():
        print('no internet connection')
    ret = subprocess.call('m2.exe')

    print('sleep 60 ')
    sleep(60)