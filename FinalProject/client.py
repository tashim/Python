import socket
import station
import _thread
from common import *
import sys
import time
"""
client module
runs TCP client socket
"""


def run(inp=INPUT_FILE,from_string=False):
    """
    runs client station socket
    """
    first_time=True
    with socket.socket() as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))

            while working:
                lk = _thread.allocate_lock()
                lk.acquire()
                time.sleep(1)
                st = str(station.Station(inp, from_string))
                print("***********client sends:",st)
                s.send(st.encode())

                if not(first_time):
                    res = s.recv(128).decode()
                    print("from server to client",res)
                else:
                    first_time = False

                lk.release()

        except:
            print("Error in client run:",sys.exc_info()[1])
        finally:
            s.close()
            print("Client closed")


working=True

if __name__ == "__main__":
    run()



