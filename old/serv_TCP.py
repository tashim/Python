import socket
from time import sleep

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
port=55151
adr='127.0.0.1'
# s.bind(('',port))
# s.settimeout(1)

# while True:
# s.connect((adr,port))
while True:
    s.sendto("ddd".encode(),(adr,port))
    # print(s.recvfrom(1024))
