import queue
import threading
import time
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
import dbMan

def window_deleted():
    print ('Good Bye')
    root.quit() # явное указание на выход из программы

class Person:

    def __init__(self,window,dic={}):
        self.wnd = window
        self.ID=''
        self.Phon = ''
        self.Email = ''
        self.Name = ''
        self.FName = ''
        self.ch_var = IntVar()
        for d in dic:
            if d == 'ID':
                self.ID=dic[d]
                self.IDL = Label(self.wnd, text=self.Phon, width=20, borderwidth=1, relief="ridge")
            if d == 'Phon':
                self.Phon=dic[d]
                self.PhonL = Label(self.wnd, text=self.Phon, width=20, borderwidth=1, relief="ridge")
            if d == 'Email':
                self.Email=dic[d]
                self.EmailL = Label(self.wnd, text=self.Email, width=20, borderwidth=1, relief="ridge")
            if d == 'Name':
                self.Name=dic[d]
                self.NameL = Label(self.wnd, text=self.Name, width=20, borderwidth=1, relief="ridge")
            if d == 'FName':
                self.FName=dic[d]
                self.FNameL = Label(self.wnd, text=self.FName, width=20, borderwidth=1, relief="ridge")
            if d == 'status':
                self.status=dic[d]

                if self.status==1:
                    st = 'פעיל'
                elif self.status==2:
                    st = 'מוקפא'
                elif self.status==3:
                    st = 'מבוטל'
                elif self.status==4:
                    st = 'סיים'
                else: st = 'none'
                self.statusL = Label(self.wnd, text=st, width=10, borderwidth=1, relief="ridge")
            if d == 'passed':
                self.passed=dic[d]
                self.ch_passed = Checkbutton(self.wnd, text='passed',
                                  variable=self.ch_var, onvalue=1, offvalue=0,
                                  command=self.ch_call,
                                  borderwidth=1)
                # self.ch_passed.setvar(self.ch_var,1)
                self.ch_var.set(self.passed)
            if d == 'timesRepeated':
                self.timesRepeated=dic[d]
                self.TimeL = Label(self.wnd, text=self.timesRepeated, width=5, borderwidth=1, relief="ridge")
            if d == 'examMark':
                self.examMark=dic[d]
                self.examMarkL = Label(self.wnd, text=self.examMark, width=5, borderwidth=1, relief="ridge")
            if d == 'freezCourse':
                self.freezCourse=dic[d]
                if self.freezCourse==1: text=' קורס מוקפא'
                else: text = 'קורס פעיל'
                self.freezCourseL = Label(self.wnd, text=text, width=8, borderwidth=1, relief="ridge")
        # Button(self.wnd, text='To do', command=get_person_list).grid( column=0, row=0 )
        self.pack()

    def ch_call(self):
        print(self.ch_var.get())
    def pack(self):
        self.PhonL.grid(column=1,row=0)
        self.EmailL.grid(column=2,row=0)
        self.NameL .grid(column=3,row=0)
        self.FNameL.grid(column=4,row=0)
        self.ch_passed.grid(column = 5, row =0)
        self.statusL.grid(column = 6, row =0)
        self.TimeL.grid(column = 7, row =0)
        self.examMarkL.grid(column = 8, row =0)
        self.freezCourseL.grid(column = 8, row =0)


def click():
    pass

def init_cbox():
    global frc
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

    Button(frc,text='update',command = cbox_ch)

def get_cbox_curs():
    db = dbMan.connnect()
    cur = db.cursor()
    cur.execute('SELECT * FROM studentsTest2.courses')
    q = cur.fetchall()
    db.close()
    name=[]
    cursID=[]
    list = [name,cursID]
    for  r in q:
        name.append(r[1])
        cursID.append(r[0])
    return list

def get_dates(index = 0):
    global cbox_list
    i = cbox_list['combo0'].current()
    # print('index =',index,'i=',1)
    cur_id = cbox_list['curs_id'][i]
    db = dbMan.connnect()
    cur = db.cursor()
    cur.execute('SELECT * FROM studentsTest2.coursecycle where courseCode = %s and coursecycle.display=1;',cur_id)
    q = cur.fetchall()
    db.close()
    name = []
    stat = []
    id = []
    for  r in q:

        id.append(r[0])
        name.append(r[2])
        stat.append(r[3])
    cbox_list['cycle_id'] = id
    cbox_list['cycle_date'] = name
    print(name)
    cbox_list['cycle_status'] = stat
    cbox_list['combo1']['values'] = name
    if name :
        cbox_list['combo1'].current(0)
    else:
        cbox_list['combo1'].set('empty')
    cbox_ch(id)

def cbox_ch(event):
    global  cbox_list
    current = cbox_list['combo1'].current()
    if cbox_list['cycle_status']:
        if cbox_list['cycle_status'][current] == 1:
            cbox_list['stat_lab']['text'] = 'מתבצע'
        elif cbox_list['cycle_status'][current] == 2:
            cbox_list['stat_lab']['text'] = 'נגמר'
        elif cbox_list['cycle_status'][current] == 3:
            cbox_list['stat_lab']['text'] = 'טרם התחיל'
        else:cbox_list['stat_lab']['text'] = cbox_list['cycle_status'][current]
    else:cbox_list['stat_lab']['text'] = 'none'
    get_person_list()

def get_person_list():
    global cbox_list,PersonList,fr
    n = 1;
    for p in PersonList:
        p.destroy()
    PersonList = []
    ID_CURS = None
    db = dbMan.connnect()
    cur = db.cursor()
    if cbox_list['cycle_id']:
        if cbox_list['combo1']['values']:
            current = cbox_list['combo1'].current()
            ID_CURS = cbox_list['cycle_id'][current]
            cur.execute(
                         """
                SELECT 
                studentspercycle.studentID,
                students.mobileNumber,
                email,
                firstName,
                familyName,
                status,        
                passed,
                timesRepeated,
                examMark,
                freezCourse
                
                FROM studentsTest2.studentspercycle
                
                inner join studentsTest2.students on studentspercycle.studentID = students.studentID
                
                
                inner join coursesperstudent on coursesperstudent.student = studentspercycle.studentID
                
                inner join coursecycle on coursecycle.code = studentspercycle.courseCycleCode
                
                where studentspercycle.courseCycleCode = %s and coursesperstudent.course = coursecycle.courseCode
                
            ;"""
                        ,ID_CURS)
            for i in cur.fetchall():
                personFrame = Frame(personFr, border=0, borderwidth=2, relief="raised")
                personFrame.grid(column=0, row=n)
                n += 1
                p = Person(personFrame,
                           {
                               'ID':i[0],
                               'Phon': i[1],
                               'Email': i[2],
                               'Name': i[3],
                               'FName': i[4],
                               'status':i[5],
                               'passed':i[6],
                               'timesRepeated':i[7],
                               'examMark':i[8],
                               'freezCourse':i[9]
                            })
                PersonList.append(personFrame)
    info['text'] = ' members of the curse '+str(len(PersonList))
    db.close()
    # print(PersonList)

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))



if __name__ == '__main__':
    cbox_list = {}
    # queue = queue.Queue()
    PersonList = []

    flag = True

    root = Tk()
    root.protocol('WM_DELETE_WINDOW',window_deleted)
    root.geometry('920x400')

    fr = Frame(root,border = 10,width=500, height=500)
    fr.pack()
    frc = Frame(fr,border = 0,borderwidth=2, relief="sunken")
    frc.pack()

    canvas = Canvas(root, borderwidth=2)
    personFr = Frame(canvas)
    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    personFr.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=personFr, anchor="nw")



    info = Label(fr,text = '')
    info.pack(fill=X)
    init_cbox()


    get_person_list()

    root.mainloop()

