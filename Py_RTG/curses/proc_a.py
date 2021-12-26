import tkinter as tk
import queue
import threading
import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
import dbMan


def window_deleted():
    print('Good Bye')
    root.quit()  # явное указание на выход из программы


class Person:

    def __init__(self, window, dic={}):
        global queue
        self.queue = queue
        self.wnd = window
        self.Phon = ''
        self.Email = ''
        self.Name = ''
        self.FName = ''
        self.ch_var = IntVar()
        for d in dic:
            if d == 'Phon': self.Phon = dic[d]
            if d == 'Email': self.Email = dic[d]
            if d == 'Name': self.Name = dic[d]
            if d == 'FName': self.FName = dic[d]
        self.PhonL = Label(self.wnd, text=self.Phon, width=20, borderwidth=2, relief="ridge")
        self.EmailL = Label(self.wnd, text=self.Email, width=10, borderwidth=2, relief="ridge")
        self.NameL = Label(self.wnd, text=self.Name, width=13, borderwidth=2, relief="ridge")
        self.FNameL = Label(self.wnd, text=self.FName, width=3, borderwidth=2, relief="ridge")
        self.ch = Checkbutton(self.wnd, text='is', variable=self.ch_var, onvalue=5, offvalue=1, command=self.set,
                              borderwidth=2, relief="ridge")
        self.ch_var.set(5)
        Button(self.wnd, text='hhhhh', command=get_person_list).grid(column=0, row=0)

    def show(self):
        self.PhonL["text"] = self.Phon
        self.EmailL["text"] = self.Email
        self.NameL["text"] = self.Name
        self.FNameL["text"] = self.FName

    def pack(self):
        self.PhonL.grid(column=1, row=0)
        self.EmailL.grid(column=2, row=0)
        self.NameL.grid(column=3, row=0)
        self.FNameL.grid(column=4, row=0)
        self.ch.grid(column=5, row=0)

    def hide(self):
        self.PhonL.pack_forget()
        self.EmailL.pack_forget()
        self.NameL.pack_forget()
        self.FNameL.pack_forget()

    def set(self):
        self.FNameL['text'] = '[' + str(self.ch_var.get()) + ']'
        # print(self.ch_var.get())
        # self.wnd.after(50, self.set)
        self.queue.put(self.FNameL['text'])


def click():
    pass


def init_cbox(frc):
    global cbox_list

    combo = Combobox(frc)
    cbli = get_cbox_curs()
    cbox_list['curs_name'] = cbli[0]
    cbox_list['curs_id'] = cbli[1]
    combo['values'] = cbox_list['curs_name']
    combo.grid(column=0, row=0)
    combo.bind("<<ComboboxSelected>>", get_dates)
    cbox_list['combo0'] = combo
    combo.current(0)  # set the selected item

    stat_lab = Label(frc)
    cbox_list['stat_lab'] = stat_lab
    stat_lab.grid(column=2, row=0)

    combo1 = Combobox(frc)
    cbox_list['combo1'] = combo1
    get_dates()

    print(cbox_list['cycle_date'])

    if combo1['values']: combo1.current(1)  # set the selected item
    combo1.grid(column=1, row=0)
    combo1.bind("<<ComboboxSelected>>", cbox_ch)

    Button(frc, text='update', command=cbox_ch)


def get_cbox_curs():
    cur.execute('SELECT * FROM studentstest2.courses')
    q = cur.fetchall()
    name = []
    cursID = []
    list = [name, cursID]
    for r in q:
        name.append(r[1])
        cursID.append(r[0])
    return list


def get_dates(index=0):
    global cbox_list
    i = cbox_list['combo0'].current()
    print('index =', index, 'i=', 1)
    cur_id = cbox_list['curs_id'][i]
    print(cur_id)
    cur.execute('SELECT * FROM studentstest2.coursecycle where courseCode = %s;', cur_id)
    q = cur.fetchall()
    name = []
    stat = []
    id = []
    for r in q:
        id.append(r[0])
        name.append(r[2])
        stat.append(r[3])
    cbox_list['cycle_id'] = id
    cbox_list['cycle_date'] = name
    cbox_list['cycle_status'] = stat
    cbox_list['combo1']['values'] = name
    if name:
        cbox_list['combo1'].current(0)
    else:
        cbox_list['combo1'].set('empty')
    cbox_ch(id)


def cbox_ch(event):
    global cbox_list
    current = cbox_list['combo1'].current()
    if cbox_list['cycle_status']:
        if cbox_list['cycle_status'][current] == 1:
            cbox_list['stat_lab']['text'] = 'מתבצע'
        elif cbox_list['cycle_status'][current] == 2:
            cbox_list['stat_lab']['text'] = 'נגמר'
        elif cbox_list['cycle_status'][current] == 3:
            cbox_list['stat_lab']['text'] = 'טרם התחיל'
        else:
            cbox_list['stat_lab']['text'] = cbox_list['cycle_status'][current]
    else:
        cbox_list['stat_lab']['text'] = 'none'
    get_person_list()


def get_person_list():
    global cbox_list, person_list, personFr, fr, canvas, vsb
    n = 1;
    # if personFr:        personFr.destroy()

    # personFr.grid(column=0, row=3)
    PersonList = []
    ID_CURS = None
    if cbox_list['cycle_id']:
        if cbox_list['combo1']['values']:
            current = cbox_list['combo1'].current()
            print(current)
            ID_CURS = cbox_list['cycle_id'][current]
            cur.execute(
                """
                    SELECT 
                    studentspercycle.studentID,
                    students.mobileNumber,
                    firstName,
                    familyName 
    
                    FROM studentstest2.studentspercycle
    
                    inner join studentstest2.students on studentspercycle.studentID = students.studentID
    
    
                    inner join coursesperstudent on coursesperstudent.student = studentspercycle.studentID
    
                    inner join coursecycle on coursecycle.code = studentspercycle.courseCycleCode
    
                    where studentspercycle.courseCycleCode = %s and coursesperstudent.course = coursecycle.courseCode
                ;"""

                , ID_CURS)

            for i in cur.fetchall():
                print(i)
                personFrame = Frame(personFr, border=0, borderwidth=2, relief="raised")
                personFrame.grid(column=0, row=n)
                n += 1
                p = Person(personFrame, {'Phon': i[0], 'Email': i[1], 'Name': i[2], 'FName': i[3]})
                p.pack()
                PersonList.append(p)


    else:
        pass


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    print('sdfsadfsaf')
    canvas.configure(scrollregion=canvas.bbox("all"))

def populate(frame):
    '''Put in some fake data'''
    for row in range(100):
        tk.Label(frame, text="%s" % row, width=3, borderwidth="1",
                 relief="solid").grid(row=row, column=0)
        t="this is the second column for row %s" %row
        tk.Label(frame, text=t).grid(row=row, column=1)


if __name__ == '__main__':

    cbox_list = {}
    db = dbMan.connnect()
    cur = db.cursor()
    person_list = []

    root = tk.Tk()
    frame0 = tk.Frame(root)
    frame0.pack()
    fr_comb = Frame(frame0)
    fr_comb.pack(side=TOP)

    canvas = tk.Canvas(frame0)
    frame = tk.Frame(canvas)
    vsb = tk.Scrollbar(frame0, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack()
    canvas.create_window((4,4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    personFr = frame
    init_cbox(fr_comb)
    # populate(frame)
    root.mainloop()