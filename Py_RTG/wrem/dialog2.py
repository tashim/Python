#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use the grid
manager to create a more complicated Windows
layout.

Author: Jan Bodnar
Last modified: July 2017
Website: www.zetcode.com
"""

from tkinter import Tk, Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style

from PIL.ImageTk import PhotoImage


class Example(Frame):

    def __init__(self):
        super().__init__()
        filename = ''

        self.initUI()

    def initUI(self):
        self.master.title("SET status don`t call")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(4, pad=7)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(13, weight=1)
        # self.rowconfigure(4, weight=1)
        # self.rowconfigure(5,  weight=1)
        # self.rowconfigure(6, pad=1)

        area = Text(self)
        area.grid(row=1, column=0, columnspan=4, rowspan=6,
                  padx=5)

        abtn = Button(self, text="Open File")
        abtn.grid(row=5, column=5)

        photo = PhotoImage(file='rted_logo.gif')
        im_l = Label(self, text='kskkskskdssscasfcasf',image=photo)
        im_l.grid(row=3,  column=5,pady=4, padx=5)
        lbl = Label(self, text="checked file:\n No file",image=photo)
        lbl.grid(sticky=W, pady=4, padx=5)



        cbtn = Button(self, text="Read")
        cbtn.grid(row=4, column=5, pady=4)


        hbtn = Button(self, text="Help")
        hbtn.grid(row=2, column=5, padx=2)

        obtn = Button(self, text="OK",image=photo)
        obtn.grid(row=1, column=5)


def main():
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()  