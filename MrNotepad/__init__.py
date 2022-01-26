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

    #min size possible
    root.resizable(True, True)
    root.minsize(600, 500)

if __name__ == '__main__':
  root = tkinter.Tk()
  program = MrNotepad(root)
  root.mainloop()