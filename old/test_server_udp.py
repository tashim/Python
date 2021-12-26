import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port=54321
adr=''
s.bind((adr,port))
s.listen(3)
print(type(s))
s.settimeout(1)
con=[]
while True:
    try:
        print('conected ',len(con))
        for co in con:
            print(co.getpeername())
        c,adr = s.accept()
        c.settimeout(1)
        print(type(c))
        print(c)
        con.append(c)
    except socket.timeout:
        pass
    for co in con:
        try:
            print(co.recv(1000))
            co.send("hi".encode())
        except socket.timeout:
            pass
        except:
            print(co.getpeername(),'disconnect')
            co.close()
            con.remove(co)
