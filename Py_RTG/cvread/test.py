from tkinter import *
from tkinter import ttk
from tkinter import messagebox


root = Tk()

root.geometry("400x400")
#^ Length and width window :D

box_value = StringVar()
cmb = ttk.Combobox(root, width="10", values=("prova","ciao","come","stai"),textvariable=box_value)
box_value.set("kkkkjkhkhk")
#^to create checkbox
#^cmb = Combobox


#now we create simple function to check what user select value from checkbox

def checkcmbo():

    print(box_value.get())
    messagebox.showinfo("nothing to show!", "you have to be choose something")




cmb.place(relx="0.1",rely="0.1")

btn = ttk.Button(root, text="Get Value",command=checkcmbo)
btn.place(relx="0.5",rely="0.1")

root.mainloop()