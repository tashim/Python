import datetime
from tkinter import *
from tkinter import messagebox, filedialog


def LOG(*args):
    if not Concole.text:
        return
    text = ''
    for i in args:
        text += ' ' + str(i)
    text = datetime.datetime.now().strftime("%H:%M:%S>") + str(text) + "\n"
    Concole.text.insert(END, text)
    Concole.text.see(END)


def LOGR(*args,end=None):
    if not Concole.textr:
        return
    if not end:
        text = ''
        for i in args:
            text += ' ' + str(i)
        text = datetime.datetime.now().strftime("%H:%M:%S>") + str(text) + "\n"
        Concole.textr.insert(END, text)
        Concole.textr.see(END)
    elif len(args)>0:
        Concole.textr.insert(END, args[0])
        Concole.textr.see(END)



class Concole():
    text = None
    textr = None

    def __init__(self, app):
        # *CONSOLE*
        frame_console = LabelFrame(app, bg='grey94')  # !!!!!!!!!!!!!!!!!!!!!!!!
        frame_console.pack(fill="both", expand=True, padx=3, pady=3)

        fr1 = Frame(frame_console)
        fr1.pack(side=LEFT, fill="both", expand=True)
        fr2 = Frame(frame_console)
        fr2.pack(side=LEFT, fill="both", expand=True)

        Concole.text = Text(fr1, fg='Black', width=140, height=90, font=("Consolas", 11), bg='white')
        scr = Scrollbar(Concole.text, command=Concole.text.yview)
        scr.pack(side=RIGHT, fill=Y)
        Concole.text.pack(fill="both", expand=True)
        Concole.text.config(yscrollcommand=scr.set)

        button_frame = Frame(fr1, height=40)
        button_frame.pack(fill="both", padx=5)
        CL = Button(button_frame, text='Clear', width=10, height=1, bg='lightgrey',
                    command=lambda: self.clear_console(Concole.text))
        CL.pack(side=LEFT, padx=25)
        SV = Button(button_frame, text='Save', width=10, height=1, bg='lightgrey',
                    command=lambda: self.save_console(Concole.text))
        SV.pack(side=LEFT, padx=25)

        Concole.textr = Text(fr2, fg='Black', width=140, height=90, font=("Consolas", 11), bg='white')
        scr = Scrollbar(Concole.textr, command=Concole.textr.yview)
        scr.pack(side=RIGHT, fill=Y)
        Concole.textr.pack(fill="both", expand=True)
        Concole.textr.config(yscrollcommand=scr.set)

        button_frame = Frame(fr2, height=40)
        button_frame.pack(fill="both", padx=5)
        CL = Button(button_frame, text='Clear', width=10, height=1, bg='lightgrey',
                    command=lambda: self.clear_console(Concole.textr))
        CL.pack(side=LEFT, padx=25)
        SV = Button(button_frame, text='Save', width=10, height=1, bg='lightgrey',
                    command=lambda: self.save_console(Concole.textr))
        SV.pack(side=LEFT, padx=25)

    def clear_console(self, widget):
        widget.delete("1.0", "end")  # clearing "Console"

    def save_console(self, widget):
        text2save = str(widget.get(1.0, END))
        if len(text2save) < 2:
            messagebox.showinfo("showinfo", "Console empty")
            return
        f = filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=(("Text files", "*.txt"),
                                                                           ("All files", "*.*"),),
                                         defaultextension='.txt')
        if f is None or len(f) < 1:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        file = open(f, 'w')
        file.write(text2save)
        file.close()  # `()` was missing.
