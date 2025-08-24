# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class MrNotepad:
    def __init__(self, root):
        self.root = root
        self.filename = None
        self.is_modified = False
        
        self.setup_window()
        self.create_widgets()
        self.create_menu()
        self.bind_events()
        
    def setup_window(self):
        #Configura a janela principal
        self.root.title('Untitled - MrNotepad')
        self.root.geometry('800x600')
        self.root.minsize(600, 500)
        self.root.resizable(True, True)
        
    def create_widgets(self):
        """Cria os widgets da interface"""
        # Área de texto com scrollbar integrada
        self.text_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            undo=True,
            font=('Consolas', 11)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Barra de status
        self.status_bar = tk.Label(
            self.root, 
            text='Ready', 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_menu(self):
        """Cria a barra de menus"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label='New', 
            accelerator='Ctrl+N', 
            command=self.new_file
        )
        file_menu.add_command(
            label='Open', 
            accelerator='Ctrl+O', 
            command=self.open_file
        )
        file_menu.add_command(
            label='Save', 
            accelerator='Ctrl+S', 
            command=self.save_file
        )
        file_menu.add_command(
            label='Save As', 
            accelerator='Ctrl+Shift+S', 
            command=self.save_as
        )
        file_menu.add_separator()
        file_menu.add_command(
            label='Exit', 
            accelerator='Alt+F4', 
            command=self.exit_program
        )
        menubar.add_cascade(label='File', menu=file_menu)
        
        # Menu Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(
            label='Undo', 
            accelerator='Ctrl+Z', 
            command=self.text_area.edit_undo
        )
        edit_menu.add_command(
            label='Redo', 
            accelerator='Ctrl+Y', 
            command=self.text_area.edit_redo
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label='Cut', 
            accelerator='Ctrl+X', 
            command=lambda: self.text_area.event_generate('<<Cut>>')
        )
        edit_menu.add_command(
            label='Copy', 
            accelerator='Ctrl+C', 
            command=lambda: self.text_area.event_generate('<<Copy>>')
        )
        edit_menu.add_command(
            label='Paste', 
            accelerator='Ctrl+V', 
            command=lambda: self.text_area.event_generate('<<Paste>>')
        )
        edit_menu.add_command(
            label='Select All', 
            accelerator='Ctrl+A', 
            command=lambda: self.text_area.tag_add(tk.SEL, '1.0', tk.END)
        )
        menubar.add_cascade(label='Edit', menu=edit_menu)
        
    def bind_events(self):
        """Configura os eventos do teclado"""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-Shift-S>', lambda e: self.save_as())
        self.text_area.bind('<<Modified>>', self.on_text_modified)
        
    def on_text_modified(self, event=None):
        """Atualiza o status quando o texto é modificado"""
        if self.text_area.edit_modified():
            self.is_modified = True
            self.update_title()
            self.text_area.edit_modified(False)
            
    def update_title(self):
        """Atualiza o título da janela"""
        name = os.path.basename(self.filename) if self.filename else 'Untitled'
        if self.is_modified:
            name += '*'
        self.root.title(f'{name} - MrNotepad')
        
    def update_status(self, message):
        """Atualiza a barra de status"""
        self.status_bar.config(text=message)
        
    def new_file(self):
        """Cria um novo arquivo"""
        if self.check_save():
            self.text_area.delete(1.0, tk.END)
            self.filename = None
            self.is_modified = False
            self.update_title()
            self.update_status('New file created')
            
    def open_file(self):
        """Abre um arquivo existente"""
        if self.check_save():
            filename = filedialog.askopenfilename(
                defaultextension='.txt',
                filetypes=[
                    ('Text Files', '*.txt'),
                    ('Python Files', '*.py'),
                    ('All Files', '*.*')
                ]
            )
            
            if filename:
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                    self.filename = filename
                    self.is_modified = False
                    self.update_title()
                    self.update_status(f'Opened: {os.path.basename(filename)}')
                except Exception as e:
                    messagebox.showerror('Error', f'Could not open file: {e}')
                    
    def save_file(self):
        """Salva o arquivo atual"""
        if self.filename:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.is_modified = False
                self.update_title()
                self.update_status(f'Saved: {os.path.basename(self.filename)}')
            except Exception as e:
                messagebox.showerror('Error', f'Could not save file: {e}')
        else:
            self.save_as()
            
    def save_as(self):
        """Salva o arquivo com um novo nome"""
        filename = filedialog.asksaveasfilename(
            initialfile='Untitled.txt',
            defaultextension='.txt',
            filetypes=[
                ('Text Files', '*.txt'),
                ('Python Files', '*.py'),
                ('All Files', '*.*')
            ]
        )
        
        if filename:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                self.filename = filename
                self.is_modified = False
                self.update_title()
                self.update_status(f'Saved as: {os.path.basename(filename)}')
            except Exception as e:
                messagebox.showerror('Error', f'Could not save file: {e}')
                
    def check_save(self):
        """Verifica se deve salvar antes de fechar/abrir novo arquivo"""
        if self.is_modified:
            response = messagebox.askyesnocancel(
                'Save Changes?',
                'Do you want to save changes before proceeding?'
            )
            
            if response is None:  # Cancel
                return False
            elif response:  # Yes
                self.save_file()
                
        return True
        
    def exit_program(self):
        """Fecha o programa"""
        if self.check_save():
            self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = MrNotepad(root)
    root.mainloop()