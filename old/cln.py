import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    text = input('text>> ')
    data = soc.sendto(text.encode(),('localhost',54321))
    # data = soc.sendto(text.encode(),('192.168.1.101',54322))
    print('sended ',data,'byte')
    data,adr=soc.recvfrom(1000)
    print(data," from",adr)

soc.close()