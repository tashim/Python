import socket
# s = socket.socket()
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=54321
adr=''
s.bind((adr,port))
s.listen(5)
s.settimeout(1)
list_client=[]
while True:
    try:
        # print("wait for connect")
        c,a=s.accept()
        print('connect', a)
        c.send('you connected'.encode())
        c.settimeout(1)
        list_client.append((c,a))
        print('list_client',len(list_client))

    except socket.timeout:
        # print('list',len(list_client))
        for con in list_client:
            try:
                # print('wait',con.getsockname())
                d = con[0].recv(100)
                print(con[1],' get ',d.decode())
            except socket.timeout:
                pass
            except:
                con[0].close()
                print(con[1],'no connect')
                list_client.remove(con)
        pass
        # print(" exept timeout")
    except:
        print('eny error')