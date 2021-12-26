
import socket

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect(('127.0.0.1',54321))
soc.close()