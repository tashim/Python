from __future__ import print_function


import re
from datetime import datetime
from tkinter import Frame, SUNKEN, FLAT, LEFT, END, Tk, NORMAL, Entry, Label, StringVar


# from tkinter.ttk import Entry, Label


class DateEntry(Frame):
    def __init__(self, master, frame_look={}, **look):
        args = dict(relief=SUNKEN, border=1)
        args.update(frame_look)
        Frame.__init__(self, master, **args)

        args = {'relief': FLAT}
        args.update(look)
        self.varDay = StringVar()
        self.varMonth = StringVar()
        self.varYear = StringVar()
        self.day = Entry(self,  width=2, **args,textvariable=self.varDay)
        self.label_1 = Label(self, text='-', **args)
        self.month = Entry(self,  width=2, **args,textvariable=self.varMonth)
        self.label_2 = Label(self, text='-', **args)
        self.year = Entry(self,  width=4, textvariable=self.varYear,**args)

        self.day.pack(side=LEFT)
        self.label_1.pack(side=LEFT)
        self.month.pack(side=LEFT)
        self.label_2.pack(side=LEFT)
        self.year.pack(side=LEFT)

        self.day.bind('<KeyRelease>', lambda e: self._check(e,1))
        self.month.bind('<KeyRelease>', lambda e: self._check(e,2))
        self.year.bind('<KeyRelease>', lambda e: self._check(e,3))
        self.set_now()

    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, END)
        entry.insert(0, cont[:-1])

    def _check(self, e , key):
        entry = e.widget
        data = entry.get()
        if e.keysym == 'Tab':
            # next_entry.focus()
            return
        if e.keysym == 'Right':
            return
        if e.keysym == 'Left':
            return
        if e.keysym =='BackSpace':
            return
        if '9' < e.keysym < '0':
            entry.delete(len(data)-1)
            return
        if key == 1:
            max = '31'
            min = '0'
            size = 2
        if key == 2:
            max = '12'
            min = '0'
            size = 2
        if key == 3:
            max = '2031'
            min = '0'
            size = 4
        for i in data:
            if not i.isdigit():  data = data.replace(i, '')
        if  data != '' and e.keysym == 'Up':
            data = str(int(data)+1)
        if data == '': data = min
        if e.keysym == 'Down' and data > '1':
            data = str(int(data)-1)
        # while len(data) > size:
        #      data = data[0:size]
        if int(data) < int(min): data = min
        if int(data) > int(max): data = max
        entry.delete(0,10)
        entry.insert(0,data)

    def get(self):
        if str(self.varDay.get())=='' or str(self.varMonth.get()) == '' or str(self.varYear.get()) == '':
            return ''
        s = str(self.varDay.get())+'-'+ str(self.varMonth.get()) + '-' + str(self.varYear.get())
        # print('str = ',s)
        return s;

    def set(self,str):
        # print('data set',str)
        str = str.strip()
        r = re.findall('\d+',str)
        # print(r)
        if len(r[2]) == 4:
            self.varYear.set( r[2])
            self.varMonth.set( r[1])
            self.varDay.set( r[0])
        if len(r[0]) == 4:
            self.varYear.set(r[0])
            self.varMonth.set(r[1])
            self.varDay.set(r[2])
        # print(self.get())

    def getMonth(self):
        return self.varMonth

    def setMonth(self,mon):
        self.varMonth(mon)
        return self.varMonth(mon)

    def set_now(self):
        today = datetime.now()
        # print(today.year)
        self.varYear.set(today.year)
        self.varMonth.set(today.month)
        self.varDay.set(today.day)
        return today.strftime('%d-%m-%Y')

    def now(self):
        today = datetime.now()
        return today.strftime('%d-%m-%Y')


class EntryNumber(Entry):
    def __init__(self, master, **look):
        args = dict(relief=SUNKEN, border=1)
        args.update(look)
        Entry.__init__(self, master, **look)
        args = {'relief': FLAT}
        args.update(look)
        self.bind('<KeyRelease>', self.keypressed)
        self.min = 1
        self.max = 20
    def keypressed(self,e):
        data = self.get()
        if e.keysym == 'Tab':
            # next_entry.focus()
            return
        if e.keysym == 'Right':
            return
        if e.keysym == 'Left':
            return
        if e.keysym =='BackSpace':
            return
        if '9' < e.keysym < '0':
            self.delete(len(data)-1)
            return
        for i in data:
            if not i.isdigit():  data = data.replace(i, '')
        if  data != '' and e.keysym == 'Up':
            data = str(int(data)+1)
        if data == '': data = min
        if e.keysym == 'Down' and data > '1':
            data = str(int(data)-1)
        if int(data) < int(self.min): data = min
        if int(data) > int(self.max): data = max
        self.delete(0,10)
        self.insert(0,data)

    def set_max(self,max): self.max = max

    def set_min(self,min): self.min = min

class UrlEntry(Entry):
    def __init__(self, master,row, **look):
        args = dict(relief=SUNKEN, border=1)
        args.update(look)
        Entry.__init__(self, master, **look)
        args = {'relief': FLAT}
        args.update(look)
        self.bind('<KeyRelease>', lambda e: self.keypressed(e,row))
        self.min = 1
        self.max = 20

    def keypressed(self,e,row):
        # print(row)
        if not row['lessVar'].get().isdigit():
            if row['lessVar'].get() !=  '':
                row['lessVar'].set(str(row['lesson']))
        if row['urlVar'].get()!=row['url'] or row['lessVar'].get()!=str(row['lesson']):
            if not row['stat']:
                row['buttom'].grid(column=14,row=row['i'])
                row['stat']=True
        else:
            if row['stat']:
                row['buttom'].grid_forget()
                row['stat']=False

def go():
    # print('go ffff',dentry.get())
    dentry.set('2020-7-22')
    print('go ffff', dentry.get())



if __name__ == '__main__':
    win = Tk()
    win.title('DateEntry demo')

    # dentry = DateEntry(win,30, border=0)
    dentry = DateEntry(win, font=('Helvetica', 40, NORMAL), border=0)
    dentry.pack()
    EntryNumber(win, font=('Helvetica', 40, NORMAL), border=0).pack()
    win.bind('<Return>', lambda e:go() )
    win.mainloop()