import threading
import time
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from exel import *
import tkinter as tk

def show_but():
    if len(filename)<3:
        buttonR.pack_forget()
        buttonS.pack_forget()
        buttonW.pack_forget()
        lab.config(text="checked file:\n None")
    else:
        buttonR.pack(expand=True, side=LEFT, padx=7,fill=X)
        lab.config(text="checked file:"+'\n'+filename)

        if not list:
            buttonS.pack_forget()
            buttonW.pack_forget()
        else:
            buttonS.pack(expand=True,fill=X, side=LEFT, padx=7)
            buttonW.pack(expand=True,fill=X, side=LEFT, padx=7)

def read_file():
    global  filename,list
    list = getlist(filename)
    if not list:
        text.insert(E,'\n Error read file')
        return
    text.insert(E,'\n readed '+str(len(list))+' items')
    text.insert(E,'\n keys list from exel:\n')
    for lk in list[0]:
        text.insert(END,' ; '+lk)
    show_but()
    return

def show():
    if not list:
        if not list:
            text.insert(E, '\n No data')
            return
    n=0
    for lk in list:
        n+=1
        text.insert(E,'\n '+str(n)+'=='+lk['telefon']+' : '+lk['email'])
    text.insert(E,'\n items:'+str(len(list)))
    text.see(END)

def pthread():
    e1.set()
    FDButton['state'] = 'disable'
    write_db()
    FDButton['state'] = 'normal'
    e1.clear()

def st():
    t2 = threading.Thread(target=pthread)
    t2.start()

def write_db():
    rd = {'insert':0,'errors':0,'act':0,'update':0}
    global  list
    if not list:
        text.insert(END, "no Data readed")
        return
    if not dbMan.connnect():
        text.insert(END, "error connection to DB")
        return
    buttonR.pack_forget()
    buttonW.pack_forget()
    buttonS.pack_forget()
    lab['text']='wait...'
    temp =''
    n=0
    for lk in list:
        rez = dbMan.input(lk)
        n +=1
        if 'error' in rez:
            rd['errors'] += 1
            text.insert(END,'\nerror ')
        elif 'insert' in rez:
            rd['insert'] += 1
            text.insert(END,'\ninsert ')
        elif 'OK' in rez:
            rd['act'] += 1
            text.insert(END,'\nOK ')
        else:
            rd['update'] += 1
            text.insert(END,'\nUpdate ')
        text.insert(END,'\n'+str(n)+ '=='+lk['telefon']+','+lk['email'])
        text.insert(END,'\n'+str(rd))
        text.see(END)
    text.insert(END,'\nDB Updated ')
    text.insert(END, str(len(list)))
    text.see(END)
    list = None
    show_but()

    dbMan.con_close()

def callFDialog():
    global filename,list
    list=None
    filename = ''
    filename = askopenfilename(filetypes = (("Exel files", "*.xls") , ))
    if len(filename)<3:
        filename = ''
        text.insert(E, '\nnot file not opened')
        list = None
        # text.delete(0.0,END)
    elif filename[-4:] != '.xls':
        filename = ''
        text.insert(E,'\nnot xls file')
        list = None
    else:
        text.insert(END,'\nopened file:'+filename)
    show_but()

def clean_text():
    text.delete(2.0,E)

def update_clock():
    now = time.strftime("%H:%M:%S")
    lableTime['text']=now
    root.after(1000, update_clock)

def on_closing():
    if e1.is_set():
        if  messagebox.askokcancel("Quit", "process is run\nDo you want to quit?"):
            root.destroy()
    else:
        root.destroy()

if __name__ == "__main__":
    root = Tk()
    filename = ''
    list = None
    photo = PhotoImage(file='rt_logo.gif')
    root.title('SET status don`t call')
    # root.minsize(600,360)
    # root.maxsize(600,360)

    frameLeft = Frame(root)
    frameRigth = Frame(root)
    frameR1 = Frame(frameRigth)
    frameR2 = Frame(frameRigth)

    im_l = Label(frameLeft, image=photo)
    lableTime = Label(frameLeft,text='time', fg = "red", font = "Times 18 bold")
    text = Text(frameR1,wrap=WORD)

    FDButton = Button(frameR2, text='File Open', command=callFDialog, height=3)
    buttonR = tk.Button(frameR2, text='Start READ File',padx=7, pady=2, command=read_file, height=3)
    buttonS = tk.Button(frameR2, text='Show data',padx=7, pady=2, command=show, height=3)
    buttonW = tk.Button(frameR2, text='Write to DB', command=st, height=3)
    buttonClean = tk.Button(frameR1, text='clean', command=clean_text)
    lab = Label(frameRigth,text='"checked file:\n None"', fg = "red", font = "Times 18 bold")

    scroll = Scrollbar(frameR1,command=text.yview)
    text.config(yscrollcommand=scroll.set)
    # root.geometry("550x550+10+15")
    # button1.pack(  padx=7, pady=2)
    frameLeft.pack(side=LEFT)
    frameRigth.pack(side=RIGHT)
    lab.pack(fill=X,side=TOP)
    frameR1.pack(side=TOP)
    frameR2.pack(side=BOTTOM,fill=X)

    scroll.pack(side=RIGHT, fill=Y)
    lableTime.pack()
    im_l.pack(fill=BOTH,side=LEFT)
    text.pack( fill =BOTH )
    buttonClean.place(x=380,y=0)
    FDButton.pack(expand=True,fill=X, side=LEFT)
    show_but()
    text.insert(0.0,'select file to read')

    e1 = threading.Event()
    e1.clear()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    update_clock()
    root.mainloop()
