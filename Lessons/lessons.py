#python3
#
import os
# import threading
# import urllib
from datetime import datetime
# from threading import Thread
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox
from dbMan import connect, con_close, get_cursCycle, get_curses, get_lessons, getStudents, get_visit, \
    getLocateList, getMark, db_update, db_saveMark


def on_save(args=0):
    for w in root.winfo_children():
        for w2 in w.winfo_children():
            for w3 in w2.winfo_children():
                if 'checkbox' in w3.winfo_name():
                    # print(w2.winfo_name(),'===',w3.winfo_name())
                    w3.on_update()
                if 'editbox'  in w3.winfo_name() :
                        db_saveMark(w3)
                        # print(w3.winfo_name())
    onSelect(1)
    pass

def on_back(args=0):
    for w in root.winfo_children():
        for w2 in w.winfo_children():
            for w3 in w2.winfo_children():

                if 'checkbox' in w3.winfo_name():
                    w3.back()
                elif 'ed' in w3.winfo_name():
                    print(w2.winfo_name(), '===', w3.winfo_name())
    # bSave.pack_forget()
    # bBack.pack_forget()
    onSelect(1)
    pass


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
# class check ================================================================================
class CheckBox(Checkbutton):
    def __init__(self,frame,data,**args):
        self.var=IntVar()
        Checkbutton.__init__(self,frame,variable=self.var,**args, command=self.cb)
        # self.var=self.var
        self.data = data
        self.start_v=get_visit(data[0],data[1],data[2])
        self.var.set(self.start_v)
        # print(self.start_v)

    def cb(self):
        pass

    def back(self):
        self.var.set(self.start_v)


    def on_update(self):
        db_update(self.data[0],self.data[1],self.data[2],self.var.get())
        pass


# class check end ============================================================================
# class editbox   ============================================================================
class Editbox(Entry):
    # base class for validating entry widgets

    def __init__(self, master,st_ID,Mark,courseCode,notTest=None,  **kw):
        Entry.__init__(self, master, **kw)
        self.courseCode=courseCode
        self.eMark = Mark[0]
        self.pMark = Mark[1]
        self.st_ID=st_ID
        self.notTest = notTest
        self.value=0
        if self.notTest :
            self.value = str( self.pMark )
        else:
            self.value = str( self.eMark )
        self.__variable = StringVar()
        self.__variable.set(self.value)
        self.__variable.trace("rwua", self.__callback)
        self.config(textvariable=self.__variable)

    def __callback(self, *dummy):
        value = self.__variable.get()
        newvalue = self.validate(value)
        if newvalue is None:
            self.__variable.set(self.value)
        elif newvalue != value:
            self.value = newvalue
            self.__variable.set(newvalue)
        else:
            self.value = value

    def validate(self, value):
         try:
            if value == '': return 0
            if value:
                v = int(value)
                if v > 110:
                    return  None
            return int(value)
         except ValueError:
            return None

# class editbox end =========================================================================



def onSelectLocation(event):
    global courses
    code = locateList['code'][locateCombo.current()]
    courses = get_cursCycle(code)
    coursCycle['values'] = courses['name']
    if len(coursCycle['values'])>0:
        coursCycle.current(0)
    onSelect(None)


def onSelect(event=None):
    global courses
    global  canvas
    # bBack.pack_forget()
    # bSave.pack_forget()
    code = 0
    courseCode=-1
    labelCours['text'] = "Read DATA"
    if len(courses['code'])>0:
        code = courses['code'][coursCycle.current()]
        courseCode = courses['courseCode'][coursCycle.current()]
    les = get_lessons(code)
    students = getStudents(code)
    if canvas: canvas.destroy()
    if courses['code'][0] > 0:
        labelCours['text'] = courses['name'][coursCycle.current()]
    else:
        labelCours['text'] = "No cours"
        return None

    canvas = Canvas(root, borderwidth=5)
    firstFrame = Frame(canvas)
    vsby = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
    vsbx = Scrollbar(canvas, orient=HORIZONTAL, command=canvas.xview)
    canvas.configure(yscrollcommand=vsby.set)
    canvas.configure(xscrollcommand=vsbx.set)
    firstFrame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    vsby.pack(side="right", fill=BOTH)
    vsbx.pack(side="bottom", fill=BOTH)

    n=10
    col = 3
    Label(firstFrame,font=font, borderwidth=4, relief="ridge", text= ' ',width=3).grid(column=col-2, row=n)
    Label(firstFrame,font=font, borderwidth=4, relief="ridge", text= 'Studets tel',width=10).grid(column=col-1, row=n)
    Label(firstFrame, font=font,borderwidth=4, relief="ridge", text= 'Studets Name',width=11).grid(column=col, row=n)
    # d = datetime()
    for l in les:
        col = col + 1
        if not (les_var.get() == 0 and not 'Test' in l[7]):
            Label( firstFrame,font=font, borderwidth=4, relief="ridge", text=l[3].strftime('%d-%m-%Y'),width=8).grid(column=col, row=n)
    Label(firstFrame, font=font,borderwidth=4, relief="ridge", text= '%%',width=6).grid(column=col+1, row=n+1)
    Label(firstFrame, font=font,borderwidth=4, relief="ridge", text= 'project',width=6).grid(column=col+1+2, row=n+1)

    col =3
    n +=1
    for l in les:
        col = col + 1
        if (not 'Test' in  l[7]) and les_var.get()==0:
            pass
        else:
            Label( firstFrame,font=font,borderwidth=4, relief="ridge", text=str( l[1] )+'('+l[7]+')' ,width=8).grid(column=col, row=n,sticky=NS)
    count =0
    for stu in students:
        """      
                    students.studentID,
                    students.mobileNumber,
                    courseCycleCode,firstName,familyName ,
                    examMark,projectMark
        """
        st_ID = stu[0]
        st_number = stu[1]
        cCode = stu[2]
        st_fname = stu[3]
        st_lname = stu[4]
        st_Mark = (stu[5],stu[6])
        n = n+1
        col = 3
        count+=1
        count_l = 0
        count_v = 0
        pr = 0
        Label(firstFrame,font=font,borderwidth=4, relief="ridge",text=str(count),width=3).grid(column=col-2,row=n,sticky=NS)
        Label(firstFrame,font=font,borderwidth=4, relief="ridge",text=st_number,width=10).grid(column=col-1,row=n,sticky=NS)
        Label(firstFrame,font=font,borderwidth=4, relief="ridge",text=st_fname+' '+ st_lname,width=11).grid(column=col,row=n,sticky=NS)
        for l in les:
            col = col + 1
            lesID=l[1]
            if not 'Test' in l[7]:
                chck = CheckBox(firstFrame, (code, st_ID, lesID), onvalue=1,  font=font,
                            offvalue=0, borderwidth=4, relief="ridge",      text='')
            else:
                chck = Editbox(firstFrame, st_ID, st_Mark,courseCode, font=font, borderwidth=4, relief="ridge", width=9)
            if not (les_var.get() == 0 and not 'Test' in l[7]):
                 chck.grid(column=col,row=n, sticky=NSEW)
            if l[3].date()>datetime.now().date():
                chck.configure(state='disabled')
            else:
                if not 'Test' in l[7]:
                    count_l += 1
                    if chck.var.get():
                        count_v+=1
            chck.pack_forget()

        if count_l==0: pr =0
        else: pr = int((count_v*100)/count_l)
        Label(firstFrame, font=font, borderwidth=4, relief="ridge", text=str(pr), width=6).grid( column=col+1, row=n, sticky=NS)
        Editbox(firstFrame,st_ID,st_Mark,courseCode,notTest='p',font=font, borderwidth=4, relief="ridge",  width=6).grid( column=col+3, row=n, sticky=NS)

    canvas.create_window((4, 4), window=firstFrame)
    canvas.pack(fill=BOTH, expand=True)

def GetPass():
    global ePass,tk_pass,PASSWORD
    PASSWORD=False
    tk_pass = Tk()
    Button(tk_pass,text='Input PASSWORD',font=font2,command=on_Pass_Inter).pack(side=LEFT)
    ePass = Entry(tk_pass,show="*", width=15,font=font2)
    tk_pass.bind('<Return>', on_Pass_Inter)

    ePass.pack()
    ePass.focus()
    tk_pass.mainloop()
    return PASSWORD

def on_Pass_Inter(e=0):
    global  ePass,tk_pass,PASSWORD
    if ePass.get() == 'yuval' :
        PASSWORD=True
    else:
        messagebox.showinfo("ERROR PASSWORD", "PASSWORD NOT CORRECT")
    tk_pass.destroy()


if __name__ == '__main__':
    global courses,db,PASSWORD
    font = 'arial 12 italic bold'
    font2 = 'arial 12 italic bold '

    # if not GetPass() :        sys.exit(0)

    root = Tk()
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w*0.6, h*0.6))
    db = connect()
    # svar1 = StringVar()
    # svar2 = StringVar()
    topFrame = Frame(root,borderwidth=4, relief="ridge").pack(side=TOP,fill=BOTH)
    fr2=Frame(topFrame)
    fr2.pack()
    fr3=Frame(topFrame)
    fr3.pack()
    locateList = getLocateList()
    locateCombo = Combobox(fr2,font=font2)
    locateCombo['values']=locateList['name']
    locateCombo.current(0)
    locateCombo.grid(row=1,column=7, sticky=NSEW)
    locateCombo.bind("<<ComboboxSelected>>", onSelectLocation)

    coursCycle = Combobox(fr3,font=font2,width=60)
    coursCycle.pack(side=TOP)
    courses = get_cursCycle(-1)

    labelCours=Label(fr3,font=font2)
    labelCours.pack()
    # coursCycle['values']=courses['name']
    # coursCycle.current(0)
    # cours.bind("<<ComboboxSelected>>", onSelectCours)
    coursCycle.bind("<<ComboboxSelected>>", onSelect)
    canvas=None
    # bBack = Button(fr2,command=on_back,text='BACK',font=font)
    bSave = Button(fr2,command=on_save,text='SAVE',font=font)
    bRefresh = Button(fr2,command=onSelect,text='REFRESH',font=font)

    # bBack.grid(row=1, column=1, sticky=NSEW)
    bSave.grid(row=1, column=2, sticky=NSEW)
    bRefresh.grid(row=1, column=3, sticky=NSEW)
    les_var=IntVar()
    lesson_chck = Checkbutton(fr2, onvalue=1, font=font,variable=les_var,
                              offvalue=0, borderwidth=4, relief="ridge",
                              command=onSelect,
                    text='show lessons')
    lesson_chck.grid(row=1, column=0, sticky=NSEW)
    les_var.set(1)
    head =Frame(root)
    head.pack()
    # Label(head,text="WAIT").pack(side=BOTTOM)
    onSelectLocation(None)
    # onSelect(None)

    root.mainloop()
    con_close()