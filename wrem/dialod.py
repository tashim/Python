
from tkinter import filedialog
from tkinter import *

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno, showinfo, showwarning, showerror
import tkinter as tk

def callback1():
    name = askopenfilename()
    print( name)

def answer():
    showerror("Answer", "Sorry, no answer available")

def callback():
    if askyesno('Verify', 'Really quit?'):
        showwarning('Yes', 'Not yet implemented')
    else:
        showinfo('No', 'Quit has been cancelled')



def callback2():
    result = askcolor(color="#6A9662",
                      title="Bernd's Colour Chooser")
    print(   result)


# root = Tk()
# rot = Tk()

Button(text='Quit', command=callback).pack(fill=X)
Button(text='Answer', command=answer).pack(fill=X)
w = Label( text="Hello Tkinter!")
print(w.config)
errmsg = 'Error!'
Button(text='File Open', command=callback1).pack(fill=X)
Button(
       text='Choose Color',
       fg="darkgreen",
       command=callback2).pack(side=LEFT, padx=10)
Button(text='Quit',
       command=quit,
       fg="red").pack(side=LEFT, padx=10)
logo = tk.PhotoImage(file="overview_replacement.gif")

counter = 0


def counter_label(label):
    def count():
        global counter
        counter += 1
        label.config(text=str(counter))
        label.after(1000, count)

    count()

def var_states():
   print("male: %d,\nfemale: %d" % (var1.get(), var2.get()))
r =Tk()
Label(r, text="Your sex:").grid(row=0, sticky=W)
var1 = IntVar()
Checkbutton( r,text="male", variable=var1).grid(row=1, sticky=W)
var2 = IntVar()
Checkbutton(r, text="female", variable=var2).grid(row=2, sticky=W)
Button(r, text='Quit', command=r.quit).grid(row=3, sticky=W, pady=4)
Button( r,text='Show', command=var_states).grid(row=4, sticky=W, pady=4)

w1 = tk.Label( image=logo,
               compound = tk.CENTER,
                text="text w1").pack(side="right",pady=10)

explanation = """At present, only GIF and PPM/PGM
formats are supported, but an interface 
exists to allow additional image file
formats to be added easily."""

w2 = tk.Label(
              justify=tk.LEFT,
              padx = 200,
              text=explanation).pack(side="left")
# w.pack()

counter_label(w)

class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)
if __name__ == '__main__':
   root = Tk()
   lng = Checkbar(root, ['Python', 'Ruby', 'Perl', 'C++'])
   tgl = Checkbar(root, ['English','German'])
   lng.pack(side=TOP,  fill=X)
   tgl.pack(side=LEFT)
   lng.config(relief=GROOVE, bd=2)

def allstates():
   print(list(lng.state()), list(tgl.state()))
Button(root, text='Quit', command=root.quit).pack(side=RIGHT)
Button(root, text='Peek', command=allstates).pack(side=RIGHT)

mainloop()