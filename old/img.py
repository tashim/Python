from tkinter import *
from tkinter.messagebox import showinfo

from PIL import ImageTk, Image
import os

def helloCallBack():
    showinfo("Hello Python", "Hello World")


root = Tk()
img = ImageTk.PhotoImage(Image.open("MicrosoftLogo.scale-100.png"))
panel = Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
but = Button(root, text ="Hello", command = helloCallBack)
but.pack()
root.mainloop()