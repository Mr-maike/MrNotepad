# -*- coding: utf-8 -*-
from msilib.schema import Icon
import os
from tkinter import *
import tkinter.filedialog

class MrNotepad:
  def __init__(self, root):
    root.title('Untitled - MrNotepad')
    root.geometry('600x500')

    self.root = root
    self.filename = None

    self.textarea = tkinter.Text(self.root, undo=True)
    self.scroll = tkinter.Scrollbar(root, command=self.textarea.yview)
    self.textarea.configure(yscrollcommand=self.scroll.set)
    self.textarea.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
    self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    self.menubar = Menubar(self)

    #min size possible
    root.resizable(True, True)
    root.minsize(600, 500)

  def set_window(self, name=None):
    if name:
      self.root.title(name + ' - MrNotepad')
    else:
      self.root.title('Untitled* - MrNotepad')
  
  #Commands
  def new_file(self):
    self.textarea.delete(1.0, tkinter.END)
    self.filename = None
    self.set_window()

  def open_file(self):
    self.filename = tkinter.filedialog.askopenfilename(
      defaultextension='.txt',
      filetypes=[('All Files', '*.*'),
                 ('Text Files', '*.txt')])
    
    if self.filename:
      self.textarea.delete(1.0, tkinter.END)
      try:
        with open(self.filename, 'r') as fr:
          self.textarea.insert(1.0, fr.read())
      except FileNotFoundError:
        return
      except:
        return
      self.set_window(os.path.basename(self.filename))
  
  def save_as(self):
    try:
        new_file = tkinter.filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                           ("Text Files", "*.txt")])
        textarea_content = self.textarea.get(1.0, tkinter.END)
        with open(new_file, "w", encoding='utf-8') as f:
            f.write(textarea_content)
        self.filename = new_file
        self.set_window(os.path.basename(self.filename))
    except:
      return
  
  def exit_program(self):
    self.answer = tkinter.messagebox.askquestion('Quit','Do you Really Want to Quit?', icon='error')

    if (self.answer):
        quit()
        #print('End!')

class Menubar:
  def __init__(self, parent):
    menubar = tkinter.Menu(parent.root)
    parent.root.config(menu=menubar)

    #file menu
    filemenu = tkinter.Menu(menubar, tearoff=0)
    filemenu.add_command(label='New file', accelerator='Ctrl+N', underline=0, command=parent.new_file)
    filemenu.add_command(label='Open file', accelerator='Ctrl+O', underline=0, command=parent.open_file)
    filemenu.add_command(label='Save', accelerator='Ctrl+S', underline=0)
    filemenu.add_command(label='Save As...', accelerator='Ctrl+Shift+S', underline=1, command=parent.save_as)
    filemenu.add_command(label='Rename', accelerator='Ctrl+Shift+R', underline=0)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', accelerator='Alt+F4', command=parent.exit_program)

    menubar.add_cascade(label='File', menu=filemenu)

    #edit menu
    editmenu = tkinter.Menu(menubar, tearoff=0)

    menubar.add_cascade(label='Edit')

    #help menu
    helpmenu = tkinter.Menu(menubar, tearoff=0)

    menubar.add_cascade(label='Help')


if __name__ == '__main__':
  root = tkinter.Tk()
  program = MrNotepad(root)
  root.mainloop()