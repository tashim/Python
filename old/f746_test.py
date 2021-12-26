import socket

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
port=55151
# adr='192.168.7.2'
s.bind(('',port))
# s.settimeout(10)

while True:
    s.sendto("text".encode(), ("192.168.0.10",5001))
    print('wait recv')
    data,address = s.recvfrom(1024)
    print("get from ",address," data",data)
