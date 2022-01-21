import os
from tkinter import *
import tkinter.filedialog

class Commands:
  def saveas():
    global text
    t = text.get('1.0', 'end-1c')
    savelocation = tkinter.filedialog.asksaveasfilename()
    file1 = open(savelocation, "w+")
    file1.write(t)
    file1.close()

root = Tk()
text = Text(root)
text.grid()
#root.geometry('1200x800')
root.title('MrNotepad - Editor de Texto')

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label='New')
filemenu.add_command(label='Open')
filemenu.add_command(label='Save')
filemenu.add_command(label='Save as...', command=Commands.saveas)

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