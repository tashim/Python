import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
soc.bind(('',54321))

while True:
    print('wait...')
    data,adr = soc.recvfrom(1024)
    soc.sendto(" i get data".encode(),adr)
    print(adr)
    print(data.decode())

soc.close()