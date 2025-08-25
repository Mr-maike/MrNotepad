# -*- coding utf-8  -*-
import tkinter as tk
from core.app import MrNotepad

def main():
    #função principal que inicia a aplicação
    root = tk.Tk()
    app = MrNotepad(root)
    root.mainloop()

if __name__ == '__main__':
    main()