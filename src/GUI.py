#!/usr/bin/python

import os
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image


def openfile():
    global file
    file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select BMP File", filetypes=[("BMP Files","*.bmp")])


class Demo1:
    def __init__(self, master):
        self.master = master
        self.master.title("Fast Fourier Transform")

        self.frame = Frame(self.master)

        # self.canvas = Canvas(self.frame, width=500, height=200)
        # self.canvas.pack()

        self.int_f_Label = Label(self.frame, text="Window width:")
        self.int_f_Entry = Entry(self.frame)

        self.int_d_Label = Label(self.frame, text="Cutting threshold for frequencies:")
        self.int_d_Entry = Entry(self.frame)

        self.image_Label = Label(self.frame, text="Image:")
        self.entryText = StringVar()
        # self.image_Entry = Entry(self.frame, textvariable=self.entryText)
        self.button = Button(self.frame, text="Source", command=openfile)
        # self.entryText.set(file)

        self.int_f_Label.grid(row=0, column=0, padx=15, pady=15)
        self.int_f_Entry.grid(row=0, column=1, padx=15, pady=15)

        self.int_d_Label.grid(row=1, column=0, padx=15, pady=15)
        self.int_d_Entry.grid(row=1, column=1, padx=15, pady=15)

        self.image_Label.grid(row=2, column=0, padx=15, pady=15)
        # self.image_Entry.grid(row=2, column=1, padx=15, pady=15)
        self.button.grid(row=2, column=1, padx=15, pady=15)

        self.submit = Button(self.frame, text='Done', command=self.return_entry)
        self.new_window = Button(self.frame, text='View Images', width=25, command=self.new_window)

        self.submit.grid(columnspan=2, padx=15, pady=15)
        self.new_window.grid(columnspan=3, padx=15, pady=15)

        self.frame.pack()

    def return_entry(self):
        """Gets and prints the content of the entry"""
        global int_f
        global int_d
        int_f = self.int_f_Entry.get()
        int_d = self.int_d_Entry.get()
        # window.destroy()

    def new_window(self):
        self.newWindow = Toplevel(self.master)
        self.app = Demo2(self.newWindow)


def main():
    window = Tk()
    app = Demo1(window)
    window.mainloop()

if __name__ == '__main__':
    main()


