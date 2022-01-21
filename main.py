import os
from tkinter import *
import tkinter

root = Tk()
root.geometry('1200x800')
root.title('MrNotepad - Editor de Texto')

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label='New')
filemenu.add_command(label='Open')
filemenu.add_command(label='Save')
filemenu.add_command(label='Save as...')

filemenu.add_separator()

filemenu.add_command(label='Exit')
menubar.add_cascade(label='File', menu=filemenu)

editmenu = Menu(menubar, tearoff=False)
editmenu.add_command(label='Undo')

editmenu.add_separator()

editmenu.add_command(label='Cut')
editmenu.add_command(label='Copy')
editmenu.add_command(label='Paste')
editmenu.add_command(label='Delete')
editmenu.add_command(label='Select All')

menubar.add_cascade(label='Edit', menu=editmenu)

root.config(menu=menubar)
root.mainloop()