
import socket
import threading
from time import sleep

def thread_function(arg):
    global s
    print("Thread %s: starting", s)
    # s.settimeout(1)
    while True:
        # print("wait rec")
        m,add=s.recvfrom(1024)
        if len(m) == 1:
            try:
                print(m.decode(),end="")
            except:
                print(m,end="")
        else:
            print("stm>",m.decode())

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
port=50011
# adr='192.168.7.2'
s.bind(('',port))
# s.settimeout(1)
address=("192.168.0.132",port)
n=0
x = threading.Thread(target=thread_function, args=(s,))
x.start()

while True:

    n +=1
    inp = input("go"   +str(n)+">")
    # print("send")
    s.sendto((inp).encode(), address)
#     while True:
#         try:
#             # print("wait rec")
#             m,add=s.recvfrom(1024)
#             if len(m) == 1:
#                 print(m.decode(),end="")
#             else:
#                 print("stm>",m.decode())
#         except socket.timeout:
#               break
#               print("no answer")
