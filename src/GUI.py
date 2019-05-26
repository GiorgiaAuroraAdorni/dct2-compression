#!/usr/bin/python

from tkinter import *
from tkinter import filedialog


def openfile():
    file = filedialog.askopenfilename()
    print(file)


def return_entry():
    """Gets and prints the content of the entry"""
    int_f = int_f_Entry.get()
    int_d = int_d_Entry.get()

    print(int_f)
    print(int_d)

    window.destroy()

window = Tk()
window.title("Fast Fourier Transform")

int_f_Label = Label(window, text="Window width:")
int_f_Entry = Entry(window)

int_d_Label = Label(window, text="Cutting threshold for frequencies:")
int_d_Entry = Entry(window)

#canvas = Canvas(window, width=500, height=200)
#canvas.pack()

button = Button(window, text="Load image", command=openfile)

submit = Button(window, text="Done", command=return_entry)

int_f_Label.grid(row=0, column=0, padx=15, pady=15)
int_f_Entry.grid(row=0, column=1, padx=15, pady=15)

int_d_Label.grid(row=1, column=0, padx=15, pady=15)
int_d_Entry.grid(row=1, column=1, padx=15, pady=15)

button.grid(columnspan=2, padx=15, pady=15)
submit.grid(columnspan=3, padx=15, pady=15)


window.mainloop()



