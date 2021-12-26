#!/usr/bin/env python3

import socket
from time import sleep

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 2000        # The port used by the server
while 1:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((HOST, PORT))
        while 1:
            print('send')
            s.send(b'N,A,01@,0\n')
            data = s.recv(1020)


            print('Received', repr(data))
            # input('xxx')
            sleep(1)