
from tkinter import *
# import Tkfont
from tkinter import ttk
from tkinter.font import Font

import tk

variable = 1

root = Tk()

style = ttk.Style()

style.configure("G.TLabel", foreground="black", background="green")   # .TLabel suffix seems to be mandatory!
style.configure("Gr.TLabel", foreground="black", background="grey")

content = ttk.Frame(root)

class App:

    def __init__(self, master):
        global HowIMet

        font1 = Font(family="Helvetica", size=38)

        root.title("TV Tracker")   # Sets the title of the root window

        # C:\Users\David\Dropbox\Software\AutoHotkey\icon.ico
        # root.wm_iconbitmap('/Users/David/Dropbox/Software/AutoHotkey/icon.ico') # Sets the window icon

        TVTracker = ttk.Label(content, text="TV Tracker", font=font1)

        TheMentalist = ttk.Label(content, text="The Mentalist:   ")
        MentalistAiring = ttk.Label(content, text="Airing in 2 days", style="G.TLabel")

        HowIMet = ttk.Label(content, text="How I Met Your Mother:   ")
        HowIMetAiring = ttk.Label(content, text="Airing in 6 days")

        Awake = ttk.Label(content, text="Awake:   ")
        AwakeAiring =ttk.Label(content, text="Airing in 3 days")

        change = ttk.Button(content, text="Change", command=self.chg)

        content.grid(column=0, row=0)   # VERY IMPORTANT! NOTHING WORKS WITHOUT THIS!
        TVTracker.grid(column=0, row=0, columnspan=2)
        TheMentalist.grid(column=0, row=1)
        MentalistAiring.grid(column=1, row=1)
        HowIMet.grid(column=0, row=2)
        HowIMetAiring.grid(column=1, row=2)
        Awake.grid(column=0, row=3)
        AwakeAiring.grid(column=1, row=3)
        change.grid(column=0, row=4)

    def chg(self):
         global variable
         if variable == 1:
            variable = 2
            # Change label background (e.g. to red)
            print (str(variable))
         elif variable == 2:
            variable = 1
            # Change label background BACK to green
            print (str(variable))
         HowIMet['text']='sdds'


HowIMet=0
app = App(root)

root.mainloop()