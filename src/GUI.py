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


class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)

        self.canvas = Canvas(self.master)
        self.canvas.pack(fill=BOTH, expand=True)
        self.image = None  # none yet

        ## Load
        self.load = Image.open(file)
        w, h = self.load.size
        self.render = ImageTk.PhotoImage(self.load)  # must keep a reference to this

        # if self.image is not None:  # if an image was already loaded
        #     self.canvas.delete(self.image)  # remove the previous image

        self.image = self.canvas.create_image((w / 2, h / 2), image=self.render)

        self.master.geometry("%dx%d" % (w, h))

        # self.path = file
        # #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object
        # self.img = ImageTk.PhotoImage(Image.open(self.path))
        #
        # #The Label widget is a standard Tkinter widget used to display a text or image on the screen
        # self.panel = Label(self.frame, image=self.img)
        #
        # #The Pack geometry manager packs widgets in rows or columns
        # self.panel.grid(columnspan=2, padx=15, pady=15)#side="bottom", fill="both", expand="yes")

        self.quitButton = Button(self.frame, text='Quit', width=25, command=self.close_windows)
        self.quitButton.pack()
        self.frame.pack()

    def close_windows(self):
        self.master.destroy()


def main():
    window = Tk()
    app = Demo1(window)
    window.mainloop()

if __name__ == '__main__':
    main()


