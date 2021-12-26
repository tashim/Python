
import socket
from time import sleep

s = socket.socket()
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=54321
adr='192.168.1.101'
s.settimeout(1)
n=0

try:
    s.connect((adr,port))
    d = s.recv(100)
    print(d)
    while True:
        text = input('text')
        s.send(text.encode())
except socket.timeout:
    pass
    # print('exeption timeout')
except:
    print('else error')
else:
    s.close()