import os
from tkinter import *
import tkinter.filedialog

class Commands:
  def saveas():
    global file
    try:
      content = str(text_main.get(1.0, tkinter.END))
      file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('Text files', '*.txt'), ('all files', '*.*')))
      file.write(content)
      file.close()

    except:
      return  
  
  def save():
    global file
    try:
      if file:
        content = str(text_main.get(1.0, tkinter.END))
        with open(file, "w", encoding="utf-8") as fw:
          fw.write(content)
      
      else:
        file = tkinter.filedialog.asksaveasfile(mode="w", defaultextension='.txt', filetypes=(('Text file', '*.txt'), ('all files', '*.*')))
        content2 = text_main.get(1.0, tkinter.END)
        file.write(content2)
        file.close()

    except:
      return
  
  def open_file():
    global file
    file = tkinter.filedialog.askopenfile(initialdir=os.getcwd(), title='Select file', filetypes=(('Text file', '*.txt'), ('All files', '*.*')))
    with open(file, "r") as fr:
        text_main.delete(1.0, tkinter.END)
        text_main.insert(1.0, fr.read())
    
    root.title(os.path.basename(file))

  
  def new_file():
    global file
    file=""
    new_window = Toplevel(root)
    new_window.title('MrNotepad - New file')
    new_text = tkinter.Text(new_window)
    new_text.grid(column=0, row=1, sticky='w', padx=10, pady=10)
    #text_main.delete(1.0, tkinter.END)

root = tkinter.Tk()
logo = PhotoImage(file='MrNotepad/icons/logo.png')
root.iconphoto(False, logo)
text_main = tkinter.Text(root)
text_main.grid(column=0, row=1, sticky='w', padx=10, pady=10)
root.title('MrNotepad - Text Editor')

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label='New', command=Commands.new_file)
filemenu.add_command(label='Open', command=Commands.open_file)
filemenu.add_command(label='Save', command=Commands.save)
filemenu.add_command(label='Save as...', command=Commands.saveas)

filemenu.add_separator()

filemenu.add_command(label='Exit')
menubar.add_cascade(label='File', menu=filemenu)

#Menu edit
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