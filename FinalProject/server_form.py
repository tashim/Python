from tkinter import *
import server
import _thread
import time
"""
server_form
main form :init,run,close all
"""


def quit_all():
    """
    function quit_all stops application
    """
    server.working = False
    server.server_quit()
    root.quit()


def open_all():
    """

    function open_all -opens server thread
    :return:
    """
    _thread.start_new_thread(server.server_init,(10,))
    _thread.start_new_thread(update_frame,())

    print("open_all")


def update_frame():
    """
    updates frame of stations list
    """
    print("update_frame tread")
    while server.working:
        time.sleep(2)

        lbl0 = Label(frame, text="sid", font="Times 20 bold italic")
        lbl0.grid(row=0, column=0, rowspan=1, columnspan=1)

        lbl1 = Label(frame, text="date", font="Times 20 bold italic")
        lbl1.grid(row=0, column=1, rowspan=1, columnspan=1)

        lbl2 = Label(frame, text="time", font="Times 20 bold italic")
        lbl2.grid(row=0, column=2, rowspan=1, columnspan=1)

        lbl3 = Label(frame, text="alarm1", font="Times 20 bold italic")
        lbl3.grid(row=0, column=3, rowspan=1, columnspan=1)

        lbl4 = Label(frame, text="alarm2", font="Times 20 bold italic")
        lbl4.grid(row=0, column=4, rowspan=1, columnspan=1)

        lk = _thread.allocate_lock()
        lk.acquire()
        row_num=1
        for st in server.running_stations.items():
            x=str(st[1]).split(' ')
            for col in range(len(x)):
                lbl = Label(frame, text=x[col], font="Times 20 bold italic")
                lbl.grid(row=row_num, column=col, rowspan=1, columnspan=1)
                col+=1
            row_num += 1
        lk.release()


root = Tk()
root.geometry("400x400")
root.title("Server management")
frame = Frame(root)
frame.grid(row=2,column=0,rowspan=1,columnspan=3)

btnOpen = Button(root, text="OPEN", font = "Times 30 bold italic",command=open_all)
btnOpen.grid(row=1,column=0 ,rowspan = 1, columnspan  = 1)

btnExit=Button(root,text="EXIT",font = "Times 30 bold italic",command=quit_all)
btnExit.grid(row=1,column=1 ,rowspan = 1, columnspan  = 1)
root.mainloop()



