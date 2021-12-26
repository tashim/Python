import socket
import threading
import time
import db
import station
import sys
from common import *
import _thread
from tkinter import messagebox
"""
server module
runs TCP server for messages,
keeps alive clients
"""


def message_to_db(station):
    """
    function: message_to_db -updates station status in database
    parameters:
        station-station object
    """
    dbconn = db.sql_connection()
    db.sql_update_station_status(dbconn, (station.station_id, station.date, station.alarm1, station.alarm2))
    dbconn.close()



def accept_message(msg,conn):
    """
    function: accept_message- accepts first message from client
    parameters:
        msg -messageint from client
        conn -tuple client address and socket
    """
    try:

        st = station.Station(msg, True,conn[0],conn[1])

        if not (running_stations.__contains__(st.station_id)):
            message_to_db(st)

            st.thread = threading.Thread(target=keep_alive, args=(st,))
            st.thread.start()
            print('accept ',st.addr,st.socket)
            running_stations[st.station_id] =st

        else:
            messagebox.showinfo("Error", "Station already running")

    except:
        print("Error in:",sys.exc_info()[1])


def keep_alive(st):
    """
    function keep_alive-keeps client alive
    parameters:
        st -running station object
    """

    while working:
        time.sleep(6)
        lk = _thread.allocate_lock()
        lk.acquire()
        try:
            st.socket.sendall("keep_alive".encode())
            msg = st.socket.recv(128).decode()
            print("*************in keep alive:",msg)
            running_stations[st.station_id]=station.Station(msg,True,st.socket,st.addr,st.thread)
            message_to_db(running_stations[st.station_id])
        except:
            print("Error in server keep_alive:", sys.exc_info()[1])
        finally:
            lk.release()

    print("keep alive closed")

        #lk.release()


def server_init(clients_num):
    """
    function server_init
    :param server_port: server port
    """
    print("server init")
    try:

        s = socket.socket()
        s.bind((SERVER_HOST, SERVER_PORT))
        s.listen(5)

        while working:

            lk = _thread.allocate_lock()
            lk.acquire()
            client_and_address = s.accept()
            clients_num-=1
            msg=str(client_and_address[0].recv(128).decode("utf-8"))
            print("************new station:", msg)

            accept_message(msg,client_and_address)
            lk.release()

    except:
        print("Error in server init:",sys.exc_info()[1])
    finally:
        s.close()
    print("server closed")


def server_quit():
    """
    function server_quit-quits all stations threads
    """
    for t in running_stations.items():
        print('tread join')
        t[1].thread.join()
        print('tread end')

"""
    running_stations-dictionary of stations:staion_id+keep_alive thread
"""
running_stations={}
"""
working flag:while loops run condition
"""
working=True

if __name__ == "__main__":
    server_init(100)