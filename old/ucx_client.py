
import socket
from time import sleep

address=("192.168.1.134",5000)
# s.setblocking(False)
n=0
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    n +=1
    inp = input("go"+str(n)+">")
    # print("send")
    s.sendto((inp + "_send from PC\r\n").encode(), address)
    m,add=s.recvfrom(1000)
    print("stm>",m)
    s.close()
