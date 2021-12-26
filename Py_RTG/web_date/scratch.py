import os
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Combobox

import dbMan
from date import *
english = False
txt_tab2 = ''
txt_tab3 = ''
txt_tab1 = ''
txt_location = ''
txt_date_open = ''
txt_moning = ''
txt_evning = ''
txt_name_curs = ''
txt_peroid = ''
txt_lesson = ''
txt_tab3_header = ''
txt_butt_lang = ''

def set_define():
    global english,\
        txt_tab2 ,\
        txt_tab3,\
        txt_tab1 ,\
        txt_location ,\
        txt_date_open ,\
        txt_moning,\
        txt_evning ,\
        txt_name_curs ,\
        txt_peroid ,\
        txt_lesson ,\
        txt_tab3_header,\
        txt_butt_lang

    if not english:
        txt_tab2 = 'מסלול'
        txt_tab3 = 'קורסים'
        txt_tab1 = 'List by Curs'
        txt_location = 'סניף'
        txt_date_open = 'תאריך פתיחה'
        txt_moning = 'בוקר'
        txt_evning = 'ערב'
        txt_name_curs = 'שם הקורס'
        txt_peroid = 'שעות'
        txt_lesson = 'מפגשים'
        txt_tab3_header = 'ניהול קורסים'
        txt_butt_lang = 'עברית'
    else:
        txt_tab3_header = 'Curs manage'
        txt_lesson = 'Lesson '
        txt_tab2 = 'Route'
        txt_tab3 = 'CURSES'
        txt_tab1 = 'List by Curs'
        txt_location = 'Location'
        txt_moning = 'moning'
        txt_evning = 'evning'
        txt_date_open = 'Date open '
        txt_name_curs = 'Name Curs'
        txt_peroid = 'Peroid'
        txt_butt_lang = 'english'



from text import *

def window_deleted():
    print('Good Bye')
    root.quit()  # явное указание на выход из программы

def get_cbox_curs():
    try:
        db = dbMan.connnect()
        cur = db.cursor()
        cur.execute('SELECT * FROM courses')
        db.close()
    except:
        messagebox.showerror('Error', "\nCann`t read DB")
    q = cur.fetchall()
    name = []
    cursID = []
    hours = []
    url = []
    list = [name, cursID,hours,url]
    for r in q:
        name.append(r[1])
        cursID.append(r[0])
        hours.append(r[2])
        url.append(r[4])
    return list

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

class ButtonDelete(Button):
    def __init__(self,master,id,tab,**data):
        Button.__init__(self,master,data)
        self.tab=tab
        self.id=id
        self['text']='Delete'
        self['command']=self.cmd
    def cmd(self):
        global  mutex
        if  mutex: return
        # print(self.id)
        if messagebox.askokcancel("Worning",'\nDelete item'):
            query ="DELETE    FROM    coursecycle  WHERE(code = %s );"
            try:
                db = dbMan.connnect()
                cur = db.cursor()
                cur.execute(query,self.id)
                db.commit()
                db.close()
                messagebox.showinfo('DELETE','\nDeleted from DB')
            except:
                messagebox.showerror('Error',"\nCann`t DELETE from DB")
            if self.tab==1: set_list_tab1(1)
            else: set_list_tab2(2)

class ButtonEdit(Button):
    def __init__(self,master,i,row,tab,**data):
        Button.__init__(self,master,**data)
        self.tab = tab
        self.row=row
        self.id=i[4]
        self.date = i[1]
        self.peroid = i[5]
        self.locat = i[6]
        self['text']='Edit'
        self['command']=self.cmd

    def cmd(self):
        global  mutex
        if  mutex: return
        else: mutex = True
        self.edit_itm = {}
        self.edit_itm['Date']= DateEntry(self.master, font=('Helvetica', 11, NORMAL), border=0)
        self.edit_itm['Date'].set(self.date.strftime('%d-%m-%Y'))
        self.varPeroid = IntVar()
        self.edit_itm['Peroid'] = Checkbutton(self.master,
            text=txt_evning, variable=self.varPeroid, onvalue=1, offvalue=0,width=8,
            font=font, command=self.onCheck)
        self.varPeroid.set(not self.peroid)
        self.onCheck()
        self.edit_itm['Location']=Combobox(self.master, width=18,font=font)
        self.setLocation()
        for i in  range(0,len( self.edit_itm['Location']['values'] )):
            if self.edit_itm['Location']['values'][i] == self.locat:
                self.edit_itm['Location'].current(i)
                break
        self.edit_itm['Date'].grid(column = 11, row=self.row )
        self.edit_itm['Peroid'].grid(column = 13, row=self.row )
        self.edit_itm['Location'].grid(column = 14, row=self.row )
        self.edit_itm['OK']=Button(self.master,text='OK',command=self.onOk,width=4)
        self.edit_itm['OK'].grid(column=7, row=self.row)
        self.edit_itm['Cancel']=Button(self.master,text='Cansel',command=self.onCancel,width=4)
        self.edit_itm['Cancel'].grid(column=8, row=self.row)

    def onCheck(self):
        # print(self.varPeroid.get())
        if self.varPeroid.get() == 1:
            self.edit_itm['Peroid']['text']=txt_moning
        else:    self.edit_itm['Peroid']['text']=txt_evning

    def setLocation(self):
        try:
            db = dbMan.connnect()
            cur = db.cursor()
            cur.execute('SELECT * FROM Locations;')
            db.close()
        except:
            messagebox.showerror('Error', "\nCann`t READ from DB")

        q = cur.fetchall()
        self.LocatList = {}
        LocatName = []
        LocatID = []
        for i in q:
            LocatName.append(i[1])
            LocatID.append(i[0])
        self.LocatList['locatName']=(LocatName)
        self.LocatList['locatID']=(LocatID)
        self.edit_itm['Location']['values']=self.LocatList['locatName']

    def onOk(self):
        peroid = not self.varPeroid.get()
        locat = self.LocatList['locatID'][self.edit_itm['Location'].current()]
        date = self.edit_itm['Date'].get()
        date = datetime.strptime(date,'%d-%m-%Y')
        if date.month+3 >12 :
            m = date.month+3 - 12
            y = date.year+1
        else:
            m = date.month + 3
            y = date.year
        date2 = datetime.strptime(str(date.day)+'-'+str(m)+'-'+str(y),'%d-%m-%Y');
        #
        # print(  self.id,
        #         date ,
        #         date2 ,
        #         peroid,
        #         locat )
        query = \
            """ 
            UPDATE  coursecycle SET
                    openDate = %s,
                    endDate = %s,
                    updateOpendate = %s,
                    display = 0,
                    peroid = %s,
                    location = %s
            WHERE code =%s;
            """
        try:
            db = dbMan.connnect()
            cur = db.cursor()
            cur.execute(query, (date, date2, date, peroid, locat,self.id))
            db.commit()
            db.close()
            messagebox.showinfo('UPDATE','\nUpdeted  DB')
        except:
            messagebox.showerror('Error', "\nCann`t Update  DB")
        if self.tab==1: set_list_tab1(1)
        else: set_list_tab2(2)

        self.onCancel()

    def onCancel(self):
        global mutex
        for i in self.edit_itm:
            self.edit_itm[i].destroy()
        mutex = False

class ButtonUpdate(Button):
    def __init__(self,master,tab,**data):
        Button.__init__(self,master,data)
        self['command']=self.cmd
        self.tab=tab
    def cmd(self):
        global  mutex
        mutex = False
        if self.tab==1: set_list_tab1(1)
        elif self.tab==3: set_list_tab3()
        else: set_list_tab2(2)

class CursCombo(Combobox):
    def __init__(self,master,**args):
        Combobox.__init__(self,master,**args)
        self.list = get_cbox_curs()
        self['values'] = self.list[0]
        self.current(0)

class ButtonInsert(Button):
    def __init__(self,master,items,tab,**data):
        Button.__init__(self,master,data)
        self.items = items
        self.tab=tab
        self['text']='Insert'
        self['command']=self.cmd
        self.new_itm = {}

    def cmd(self):
        global  mutex
        if  mutex: return
        else: mutex = True
        if self.tab == 1:
            headerTab1.pack_forget()
            self.frame = Frame(firstFrame)
            self.frame.pack(side=TOP, fill=BOTH)
        else:
            headerTab2.pack_forget()
            self.frame = Frame(secondFrame)
            self.frame.pack(side = TOP,fill=BOTH)
        # Head
        self.new_itm['h_Name']=Label(self.frame, text=txt_name_curs, width=18, borderwidth=1, relief="ridge", font=font)
        self.new_itm['h_Date']=Label(self.frame, text=txt_date_open,  borderwidth=1, relief="ridge", font=font)
        self.new_itm['h_Lesson']=Label(self.frame, text=txt_lesson,  borderwidth=1, relief="ridge", font=font)
        self.new_itm['h_Peroid']=Label(self.frame,text=txt_peroid, borderwidth=1, relief="ridge",font=font)
        self.new_itm['h_Location']=Label(self.frame,text=txt_location, width=18, borderwidth=1, relief="ridge",font=font)
        self.new_itm['h_URL']=Label(self.frame, text="URL",  borderwidth=1, relief="ridge", font=font)
        # members
        self.new_itm['Name']= CursCombo(self.frame,font=font)
        self.new_itm['Name'].bind("<<ComboboxSelected>>", self.lesson_by_curs)
        self.new_itm['Date']= DateEntry(self.frame, font=('Helvetica', 10, NORMAL), border=0)
        self.new_itm['Lesson']=Label(self.frame, text='   ',  borderwidth=1, relief="ridge", font=font)
        self.varPeroid = IntVar()
        self.new_itm['Peroid'] = Checkbutton(self.frame,
            text=txt_evning, variable=self.varPeroid, onvalue=1, offvalue=0,width=8,
            font=font, command=self.onCheck)
        self.new_itm['Location']=Combobox(self.frame, width=18,font=font)

        self.new_itm['URL']=Label(self.frame, text=' ', borderwidth=1, relief="ridge", font=font)
        self.setLocation()
        self.new_itm['Location'].current(0)
        self.lesson_by_curs(1)
        r = hc = mc =0
        for i in self.new_itm:
            if 'h_' in i:
                r=1
                hc +=1
                c=hc
            else:
                r = 2
                mc +=1
                c = mc
            self.new_itm[i].grid(column = c+5, row=r+4 )
        self.butOK=Button(self.frame,text='OK',command=self.onOk,width=4)
        self.butOK.grid(column=1, row=6)
        self.butCancel=Button(self.frame,text='Cansel',command=self.onCancel,width=4)
        self.butCancel.grid(column=2, row=6)
        Label(self.frame,text='  ').grid(column=0,row=6)

    def onCheck(self):
        # print(self.varPeroid.get())
        if self.varPeroid.get() == 1:
            self.new_itm['Peroid']['text']=txt_moning
        else:
            self.new_itm['Peroid']['text']=txt_evning
    def setLocation(self):
        try:
            db = dbMan.connnect()
            cur = db.cursor()
            cur.execute('SELECT * FROM Locations;')
            q = cur.fetchall()
            db.close()
        except:
            messagebox.showerror('Error', "\nCann`t READ from DB")
        self.LocatList = {}
        LocatName = []
        LocatID = []
        for i in q:
            LocatName.append(i[1])
            LocatID.append(i[0])
        self.LocatList['locatName']=(LocatName)
        self.LocatList['locatID']=(LocatID)
        self.new_itm['Location']['values']=self.LocatList['locatName']
    def lesson_by_curs(self,e):
        index = self.new_itm['Name'].current()
        id = self.new_itm['Name'].list[1][index]
        try:
            db = dbMan.connnect()
            cur = db.cursor()
            cur.execute('select url,hours from courses where courseCode=%s ',id)
            q = cur.fetchone()
            db.close()
        except:
            messagebox.showerror('Error', "\nCann`t READ from DB")
        self.new_itm['URL']['text'] = '  '
        self.new_itm['Lesson']['text'] = '  '
        if q:
            self.new_itm['URL']['text']=q[0]
            self.new_itm['Lesson']['text']=q[1]

    def cmp(self,d1,d2):
        d1 = d1.split('-')
        d2 = d2.split('-')
        if int(d1[2]) < int(d2[2]): return  -1
        if int(d1[2]) > int(d2[2]): return  1
        if int(d1[1]) < int(d2[1]): return  -1
        if int(d1[1]) > int(d2[1]): return  1
        if int(d1[0]) < int(d2[0]): return  -1
        if int(d1[0]) > int(d2[0]): return  1
        return 0

    def month3(self,d):
        d = d.split('-')
        i = int (d[1])+3
        if i > 12 :
            i = i - 12
            y = int(d[2])+1
        else:
            y = int(d[2])
        return d[0]+'-'+str(i)+'-'+str(y)

    def onOk(self):
        index = self.new_itm['Name'].current()
        courseCode = self.new_itm['Name'].list[1][index]
        openDate = self.new_itm['Date'].get()
        today = self.new_itm['Date'].now()
        if self.cmp(openDate,today) < 0 :
            print('errorr')
            return
        endd = self.month3(openDate)
        print(openDate,endd,today)
        locat = self.LocatList['locatID'][self.new_itm['Location'].current()]
        peroid = not self.varPeroid.get()
        openDate = datetime.strptime(openDate, '%d-%m-%Y')
        endd = datetime.strptime(endd, '%d-%m-%Y')
        query =\
    """ 
    INSERT INTO coursecycle
            (courseCode,
            openDate,
            courseStatus,
            endDate,
            updateOpendate,
            OpenerName,
            display,
            peroid,
            location)
    VALUES
        (%s, %s, 0, %s, %s, 'prog', 0, %s, %s);
    """
        try:
            db = dbMan.connnect()
            cur = db.cursor()
            cur.execute(query,(courseCode,openDate,endd,openDate,peroid,locat))
            db.commit()
            db.close()
            messagebox.showinfo('INSERT','\nInserted into DB')
        except:
            messagebox.showerror('Error', "\nCann`t INSERT into DB")
        self.onCancel()

    def onCancel(self):
        global mutex
        mutex = False
        if self.tab == 2 :
            headerTab2.pack(fill=X)
            set_list_tab2(2)
        else:
            headerTab1.pack(side=TOP,fill=X)
            set_list_tab1(1)
        self.frame.destroy()

def db_select(frame,id,tab):
    # print(' tab ',tab,' id=',id)
    q_select=\
    """
    SELECT  courseName,
            openDate,
            hours,
            url,
            code,
            peroid,
            Locations.location
    FROM coursecycle
    """
    q_where=\
    """
    where   coursecycle.display=0
    """
    q_end = \
    """
        order by openDate desc;
    """
    q_join_curses= 'inner join courses on coursecycle.courseCode=courses.courseCode '
    q_join_locate= 'inner join Locations on coursecycle.location=Locations.idLocations '
    q_join_coursesperpath = 'inner join coursesperpath on coursesperpath.courseCode=coursecycle.courseCode '
    if tab == 2:
        if id == 0:
            query = q_select + q_join_curses + q_join_locate + q_where + q_end
        else:
            query = q_select + q_join_curses + q_join_locate + q_join_coursesperpath +q_where \
                    + "and pathCode = "+ str(id) +" " + q_end
    else:
        if id == 0:
            query = q_select + q_join_curses + q_join_locate + q_where + q_end
        else:
            query =  q_select + q_join_curses + q_join_locate + q_where +\
                     " and courses.courseCode = "+ str(id) +" " \
                      + q_end
    try:
        db = dbMan.connnect()
        cur = db.cursor()
        cur.execute(query)
        q = cur.fetchall()
        db.close()
    except:
        messagebox.showerror('Error', "\nCann`t READ from DB")
    #
    #   Header of Table

    Label(frame,text='  ').grid(column=0,row=9)
    Label(frame, text=txt_name_curs, width=18, borderwidth=1, relief="ridge", font=font).grid(column=10, row=20)
    Label(frame, text=txt_date_open,  borderwidth=1, relief="ridge", font=font).grid(column=11, row=20)
    Label(frame, text=txt_lesson,  borderwidth=1, relief="ridge", font=font).grid(column=12, row=20)
    Label(frame, text=txt_peroid,  borderwidth=1, relief="ridge", font=font).grid(column=13, row=20)
    Label(frame, text=txt_location, borderwidth=1, width=18, relief="ridge", font=font).grid(column=14, row=20)
    Label(frame, text="URL",  borderwidth=1, relief="ridge", font=font).grid(column=15, row=20)

    n=111
    for i in q:
        # print(i)
        if i[5]:peroid = txt_evning
        else:peroid =  txt_moning
        Label(frame,text=i[0], width=18, borderwidth=1, relief="ridge",font=font).grid(column=10,row=n)
        Label(frame,text=i[1].strftime('%d-%m-%Y'), borderwidth=1, relief="ridge",font=font).grid(column=11,row=n)
        Label(frame,text=i[2],  borderwidth=1, relief="ridge",font=font).grid(column=12,row=n)
        Label(frame,text=i[3], borderwidth=1, relief="ridge",font=font).grid(column=15,row=n)
        Label(frame,text=peroid,width=12, borderwidth=1, relief="ridge",font=font).grid(column=13,row=n)
        Label(frame, text=i[6], width=18, borderwidth=1, relief="ridge", font=font).grid(column=14, row=n)
        ButtonDelete(frame,i[4],tab,width=4).grid(column=7,row=n)
        ButtonEdit(frame,i,n,tab,width=4).grid(column=8,row=n)
        n += 1

def init_first():
    Fr1Items['childFrame']=None
    Fr1Items['combo'] = Combobox(headerTab1,font=font)
    cbli = get_cbox_curs()
    Fr1Items['curs_name'] = cbli[0]
    Fr1Items['curs_id'] = cbli[1]
    Fr1Items['combo']['values'] = Fr1Items['curs_name']
    Fr1Items['combo'].bind("<<ComboboxSelected>>", set_list_tab1)
    Fr1Items['combo'].current(0)  # set the selected item
    Fr1Items['update'] = ButtonUpdate(headerTab1,1,text='Update')
    Fr1Items['insert'] = ButtonInsert(headerTab1,Fr1Items,1,text='insert')
    Fr1Items['combo'].grid(column=10,row=10)
    Fr1Items['update'].grid(column=8,row=11)
    Fr1Items['insert'].grid(column=9,row=11)
    Label(headerTab1,text='  ').grid(column=1,row=10)
    set_list_tab1(0)
    # Button(frc, text='update', command=click)
    

def set_list_tab1(index):
    if  Fr1Items['childFrame']: Fr1Items['childFrame'].destroy()
    Fr1Items['childFrame'] = Frame(frameTab1)
    Fr1Items['childFrame'].pack(side=LEFT,fill=BOTH)
    id = Fr1Items['curs_id'][Fr1Items['combo'].current()]
    db_select(Fr1Items['childFrame'],id,1)

def init_second():
    Fr2Items['childFrame']=None

    combo = Combobox(headerTab2,font=font)
    combo.bind("<<ComboboxSelected>>", set_list_tab2)
    combo.grid(column=9,row=10)
    comboList = ['all']
    comboListId = [0]
    comboListURL = ['']
    Fr2Items['combo'] = combo
    urlLable = ttk.Label(headerTab2,text = '________',font=font)
    urlLable.grid(column=10,row=10)
    Fr2Items['urlLable'] = urlLable
    try:
        db = dbMan.connnect()
        cur = db.cursor()
        cur.execute('SELECT * FROM path;')
        db.close()
    except:
        messagebox.showerror('Error', "\nCann`t READ from DB")
    q = cur.fetchall()
    for i in q:
        comboList.append(i[1])
        comboListId.append(i[0])
        comboListURL.append(i[2])
    Fr2comboURL['ccmbListId'] = comboListId
    Fr2comboURL['comboListURL'] = comboListURL
    combo['values']=comboList
    combo.current(0)
    Fr2Items['update'] = ButtonUpdate(headerTab2,2,text='Update')
    Fr2Items['insert'] = ButtonInsert(headerTab2,Fr2Items,2,text='insert')
    Fr2Items['update'].grid(column=6,row=11)
    Fr2Items['insert'].grid(column=7,row=11)
    Label(headerTab2,text='  ').grid(column=1,row=10)
    set_list_tab2(0)

def set_list_tab2(index):
    if  Fr2Items['childFrame']: Fr2Items['childFrame'].destroy()
    Fr2Items['childFrame'] = Frame(frameTab2)
    Fr2Items['childFrame'].pack()
    id = Fr2comboURL['ccmbListId'][Fr2Items['combo'].current()]
    db_select(Fr2Items['childFrame'],id,2)
    Fr2Items['urlLable']['text'] = Fr2comboURL['comboListURL'][Fr2Items['combo'].current()]

def init_thirdTab():
    ThirdItems['HeaderText'] = Label(headerTab3,text=txt_tab3_header,font=font)
    ThirdItems['HeaderText'].pack(side=TOP)
    ButtonUpdate(headerTab3,3,text='Refresh').pack()
    ThirdItems['frame']= None
    set_list_tab3()

class CursBottom(Button):
    def __init__(self,master,row,**data):
        Button.__init__(self,master,data)
        self.row=row
        self['text']='Update'
        self['command']=self.cmd

    def cmd(self):
        # print('Update Db id=',self.row['id'])
        if not self.row['lessVar'].get().isdigit():
            self.row['lessVar'].set(str(self.row['lesson']))
            messagebox.showinfo('Error','\n'+txt_lesson+' must be number')
        else:
            self.row['lesson'] = str(self.row['lessVar'].get())
            self.row['url'] = self.row['urlVar'].get()
            query =\
            """UPDATE courses SET hours=%s,url=%s WHERE courseCode=%s"""
            db = dbMan.connnect()
            cur = db.cursor()
            try:
                cur.execute(query,(self.row['lessVar'].get(),self.row['urlVar'].get(),self.row['id']))
                db.commit()
                messagebox.showinfo('Update','\nUpdated DB')
            except:
                messagebox.showerror('Error',"\nCann`t uddate DB")
            db.close()
        if self.row['urlVar'].get() != self.row['url'] or self.row['lessVar'].get() != str(self.row['lesson']):
            if not self.row['stat']:
                self.row['buttom'].grid(column=14, row=self.row['i'])
                self.row['stat'] = True
        else:
            if self.row['stat']:
                self.row['buttom'].grid_forget()
                self.row['stat'] = False


def set_list_tab3():
    if ThirdItems['frame']:ThirdItems['frame'].destroy()
    ThirdItems['frame'] = Frame(frameTab3)
    ThirdItems['frame'].pack(fill=BOTH)
    list_base = get_cbox_curs()
    list=[]
    for i in range(0,len(list_base[0])):
        row = {}
        row['id']=list_base[1][i]
        row['Name']=list_base[0][i]
        row['lesson']=list_base[2][i]
        if not list_base[3][i]:list_base[3][i]=''
        row['url']=list_base[3][i]
        row['stat']=False
        list.append(row)

    for i in range(0,len(list)):
        lessVar=StringVar()
        urlVar=StringVar()
        Label(ThirdItems['frame'],text=list[i]['Name'],font=font).grid(column=10,row = i)
        UrlEntry(ThirdItems['frame'],list[i],width=4,textvariable=lessVar,font=font).grid(column=12,row = i)
        lessVar.set( str(list[i]['lesson']) )
        UrlEntry(ThirdItems['frame'],list[i],width=40,textvariable=urlVar,font=font,state=NORMAL).grid(column=13,row = i)
        urlVar.set(list[i]['url'])
        list[i]['i']=i
        list[i]['urlVar']=urlVar
        list[i]['lessVar']=lessVar
        list[i]['buttom']=CursBottom(ThirdItems['frame'],list[i])

        # Label(ThirdItems['frame'],text=list[3][i],font=font).grid(column=14,row = i)
def OnEntryClick(e,r):
    print('chenged',r['Name'])


def change_lang():
    global english
    english = not english
    set_define()
    langB['text'] = txt_butt_lang
    tab_control.tab(0)['text'] = txt_tab1
    tab_control.tab(1)['text'] = txt_tab2
    tab_control.tab(2)['text'] = txt_tab3
    set_list_tab1(1)
    set_list_tab2(1)
    set_list_tab3()
    ThirdItems['HeaderText']['text']=txt_tab3_header

if __name__ == '__main__':

    mutex = False
    font = 'arial 12 italic bold'
    Fr2Items = {}
    Fr1Items = {}
    Fr2comboURL = {}
    root = Tk()
    x = str(root.winfo_screenwidth()-200)
    y = str(root.winfo_screenheight()- 200)
    set_define()

    # root.protocol('WM_DELETE_WINDOW', window_deleted)
    root.geometry(x+'x'+y)
    tab_control = ttk.Notebook(root)
    langB = Button(root,text='Language',height=1,command=change_lang)
    langB.place(x=400,y=0)
    tab1 = ttk.Frame(tab_control)
    tab_control.add(tab1, text=txt_tab1)
    canvas = Canvas(tab1, borderwidth=2)
    firstFrame = Frame(canvas)
    vsby = Scrollbar(tab1, orient=VERTICAL, command=canvas.yview)
    vsbx = Scrollbar(tab1, orient=HORIZONTAL, command=canvas.xview)
    canvas.configure(yscrollcommand=vsby.set)
    canvas.configure(xscrollcommand=vsbx.set)
    firstFrame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    vsby.pack(side="right", fill=BOTH)
    vsbx.pack(side="bottom", fill=BOTH)
    canvas.pack(side="left", fill=BOTH, expand=True)
    canvas.create_window((4, 4), window=firstFrame, anchor="nw")
    frameTab1 = Frame(firstFrame)
    headerTab1 = Frame(firstFrame)
    headerTab1.pack(side=TOP,fill=BOTH)
    frameTab1 = Frame(firstFrame)
    frameTab1.pack(side=BOTTOM,fill=BOTH)


    tab2 = ttk.Frame(tab_control)
    tab_control.add(tab2, text=txt_tab2)
    canvas2 = Canvas(tab2, borderwidth=2)
    secondFrame = Frame(canvas2)
    vsby2 = Scrollbar(tab2, orient="vertical", command=canvas2.yview)
    vsbx2 = Scrollbar(tab2, orient=HORIZONTAL, command=canvas2.xview)
    canvas2.configure(yscrollcommand=vsby2.set)
    canvas2.configure(xscrollcommand=vsbx2.set)
    secondFrame.bind("<Configure>", lambda event, canvas=canvas2: onFrameConfigure(canvas2))
    vsby2.pack(side="right", fill="y")
    vsbx2.pack(side="bottom", fill="x")
    canvas2.pack(side="left", fill="both", expand=True)
    canvas2.create_window((4, 4), window=secondFrame, anchor="nw")
    frameTab2 = Frame(secondFrame)
    headerTab2 = Frame(secondFrame)
    headerTab2.pack(fill=X)
    frameTab2.pack(side=BOTTOM, fill = BOTH)

    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab3, text=txt_tab3)
    canvas3 = Canvas(tab3, borderwidth=2)
    thirdFrame = Frame(canvas3)
    vsby3 = Scrollbar(tab3, orient="vertical", command=canvas3.yview)
    vsbx3 = Scrollbar(tab3, orient=HORIZONTAL, command=canvas3.xview)
    canvas3.configure(yscrollcommand=vsby3.set)
    canvas3.configure(xscrollcommand=vsbx3.set)
    thirdFrame.bind("<Configure>", lambda event, canvas=canvas3: onFrameConfigure(canvas3))
    vsby3.pack(side="right", fill="y")
    vsbx3.pack(side="bottom", fill="x")
    canvas3.pack(side="left", fill="both", expand=True)
    canvas3.create_window((4, 4), window=thirdFrame, anchor="ne")
    headerTab3 = Frame(thirdFrame)
    headerTab3.pack(fill=X)
    frameTab3 = Frame(thirdFrame)
    frameTab3.pack()
    ThirdItems = {}

    tab_control.pack(expand=True, fill=BOTH)
    init_first()
    init_second()
    init_thirdTab()

    root.mainloop()

