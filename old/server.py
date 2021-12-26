#!/usr/bin/env python3

import socket

HOST = ''  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
b = b'0000000000000000000000000'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(10)
    s.setblocking(False)#settimeout(1)
    li=[]

    while 1:
        try:
            conn, addr = s.accept()
            li.append(conn)
        except socket.timeout:
            print("no connection timeout")
        except:
            # print("error connect")
            pass
        i = 0;
        for conn in li:
            conn.settimeout(1)
            i += 1
            try:
                data = conn.recv(1024)

            except socket.timeout:
                print(i, conn.getsockname()," no data")
            except:
                print(i, conn.getsockname(),"disconnect")
                li.remove(conn)
                conn.close()

            else:
                print(i, conn.getsockname(),data)
                b=int(13).to_bytes(1,'little')
                b.__add__(bytes(10))
                print(b)
                conn.send(b)
