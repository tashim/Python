from tkinter import *
import _thread
import client
import station
from common import *
import os.path
from shutil import copyfile
from tkinter import messagebox
"""
Displays one station data and enables running data update
"""


def send():
    """
    initiates sending station data to server
    :return:
    """
    _thread.start_new_thread(send_data,())


def get_file():
    """
    gets file name
    :return: file name with current station id
    """
    return "status{0}.txt".format(sid.get())


def send_data():
    """
    sends station data to server
    :return:
    """
    file_name = get_file()
    if not(os.path.isfile(file_name)):
        copyfile(INPUT_FILE, file_name)
    print("sending client data")
    client.run(file_name)


def client_quit():
    """
    quits client form
    :return:
    """
    client.working=False
    master.quit()


def save_file():
    """
    saves station data file
    :return:
    """
    if not(sid.get().isdigit()):
        messagebox.showinfo("Error", "Station id must be an integer number")
        return
    file_name=get_file()
    with open(file_name,"w") as file:
        file.write("{0}\n{1}\n{2}\n".format(sid.get(),alarm1_val.get(),alarm2_val.get()))
        file.close()
    btnRun.configure(state='normal')


def read_file():
    """
    reads default station data file
    :return:Station data object
    """
    st=station.Station(INPUT_FILE,False)
    check_file="status{0}.txt".format(st.station_id)
    if os.path.isfile(check_file):
        st = station.Station(check_file, False)
    return st


def change_data(ev=None):
    """
    handles changing data in form
    :param ev: event object
    :return:
    """
    if ev:
        if ev.keycode != 36 :
            btnRun.configure(state='disabled')
    else:
        btnRun.configure(state='disabled')

record=read_file()

master = Tk()
master.geometry("400x200")
master.title("Client management")

sid_val=StringVar()
sid_val.set(record.station_id)
Label(master, text="Station ID",font="Times 20 bold italic").grid(row=0,column=0)
sid=Entry(master,text=sid_val,relief=RAISED,font="Times 20 bold italic")
sid.grid(row=0,column=1)
sid.bind('<Key>',change_data)

alarm1_val=IntVar()
alarm1_val.set(record.alarm1)
Label(master, text="Alarm1",font="Times 20 bold italic").grid(row=1,column=0)
alarm1=Checkbutton(master ,font="Times 30",onvalue=1, offvalue=0, variable=alarm1_val,relief='groove',command=change_data)
alarm1.grid(row=1,column=1,sticky='W')


alarm2_val=IntVar()
alarm2_val.set(record.alarm2)
Label(master,text="Alarm2",font="Times 20 bold italic").grid(row=2,column=0)
alarm2=Checkbutton(master ,font="Times 30", onvalue=1, offvalue=0, variable=alarm2_val,relief='groove',command=change_data)
alarm2.grid(row=2,column=1,sticky='W')


frame = Frame(master)
frame.grid(row=3,column=0,rowspan=1,columnspan=2)

Button(frame, text="Save",font="Times 30 bold italic", command=save_file).grid(row=0, column=0, sticky=W, pady=6)

btnRun=Button(frame, text="Run",font="Times 30 bold italic", command=send)
btnRun.grid(row=0, column=1, sticky=W, pady=6)

Button(frame, text="Quit",font="Times 30 bold italic", command=client_quit).grid(row=0, column=2, sticky=W, pady=6)

mainloop()

