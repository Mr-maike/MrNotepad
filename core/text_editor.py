import tkinter as tk
from tkinter import scrolledtext

class TextEditor:
    def __init__(self, app):
        self.app = app
        self.create_widgets()

    def create_widgets(self):

        self.main_frame = tk.Frame(self.app.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = scrolledtext.ScrolledText(
            self.main_frame,
            wrap = tk.WORD,
            undo=True,
            font=('Consolas', 11),
            padx = 10,
            pady = 10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.status_bar = tk.Label(
            self.app.root,
            text='Ready',
            relief=tk.SUNKEN,
            anchor=tk.W,
            padx=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        def get_content(self):
            #retorna o conteudo do texto
            return self.text_area.get(1.0, tk.END)
        
        def set_content(self, content):
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, tk.content)

        def clear_content(self):
            self.text_area.delete(1.0, tk.END)

        def update_status(self, message):
            self.status_bar.config(text=message)

        def has_selection(self):
            try:
                return bool(self.text_area.tag_range(tk.SEL))
            
            except:
                return False