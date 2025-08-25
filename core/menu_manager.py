# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

class MenuManager:
    def __init__(self, app):
        self.app = app
        self.create_menubar()
        
    def create_menubar(self):
        """Cria a barra de menus completa"""
        menubar = tk.Menu(self.app.root)
        self.app.root.config(menu=menubar)
        
        self._create_file_menu(menubar)
        self._create_edit_menu(menubar)
        self._create_view_menu(menubar)
        self._create_help_menu(menubar)
        
    def _create_file_menu(self, menubar):
        """Cria o menu Arquivo"""
        file_menu = tk.Menu(menubar, tearoff=0)
        
        file_menu.add_command(
            label='New', 
            accelerator='Ctrl+N', 
            command=self.app.file_operations.new_file
        )
        file_menu.add_command(
            label='Open', 
            accelerator='Ctrl+O', 
            command=self.app.file_operations.open_file
        )
        file_menu.add_command(
            label='Save', 
            accelerator='Ctrl+S', 
            command=self.app.file_operations.save_file
        )
        file_menu.add_command(
            label='Save As', 
            accelerator='Ctrl+Shift+S', 
            command=self.app.file_operations.save_as
        )
        file_menu.add_separator()
        file_menu.add_command(
            label='Exit', 
            accelerator='Alt+F4', 
            command=self.app.file_operations.exit_program
        )
        
        menubar.add_cascade(label='File', menu=file_menu)
        
    def _create_edit_menu(self, menubar):
        """Cria o menu Editar"""
        edit_menu = tk.Menu(menubar, tearoff=0)
        
        edit_menu.add_command(
            label='Undo', 
            accelerator='Ctrl+Z', 
            command=self._undo
        )
        edit_menu.add_command(
            label='Redo', 
            accelerator='Ctrl+Y', 
            command=self._redo
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label='Cut', 
            accelerator='Ctrl+X', 
            command=self._cut
        )
        edit_menu.add_command(
            label='Copy', 
            accelerator='Ctrl+C', 
            command=self._copy
        )
        edit_menu.add_command(
            label='Paste', 
            accelerator='Ctrl+V', 
            command=self._paste
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label='Select All', 
            accelerator='Ctrl+A', 
            command=self._select_all
        )
        
        menubar.add_cascade(label='Edit', menu=edit_menu)
        
    def _create_view_menu(self, menubar):
        """Cria o menu Visualizar"""
        view_menu = tk.Menu(menubar, tearoff=0)
        
        # Futuras implementações: temas, zoom, etc.
        view_menu.add_command(label='Zoom In', command=lambda: None)
        view_menu.add_command(label='Zoom Out', command=lambda: None)
        view_menu.add_separator()
        view_menu.add_command(label='Toggle Status Bar', command=lambda: None)
        
        menubar.add_cascade(label='View', menu=view_menu)
        
    def _create_help_menu(self, menubar):
        """Cria o menu Ajuda"""
        help_menu = tk.Menu(menubar, tearoff=0)
        
        help_menu.add_command(label='About MrNotepad', command=self._show_about)
        help_menu.add_command(label='Documentation', command=lambda: None)
        
        menubar.add_cascade(label='Help', menu=help_menu)
        
    # Métodos de edição
    def _undo(self):
        """Desfaz a última ação"""
        try:
            self.app.text_editor.text_area.edit_undo()
        except tk.TclError:
            pass
            
    def _redo(self):
        """Refaz a última ação"""
        try:
            self.app.text_editor.text_area.edit_redo()
        except tk.TclError:
            pass
            
    def _cut(self):
        """Corta o texto selecionado"""
        if self.app.text_editor.has_selection():
            self.app.text_editor.text_area.event_generate('<<Cut>>')
            
    def _copy(self):
        """Copia o texto selecionado"""
        if self.app.text_editor.has_selection():
            self.app.text_editor.text_area.event_generate('<<Copy>>')
            
    def _paste(self):
        """Cola o texto da área de transferência"""
        self.app.text_editor.text_area.event_generate('<<Paste>>')
        
    def _select_all(self):
        """Seleciona todo o texto"""
        self.app.text_editor.text_area.tag_add(tk.SEL, '1.0', tk.END)
        self.app.text_editor.text_area.mark_set(tk.INSERT, '1.0')
        
    def _show_about(self):
        """Mostra informação sobre o programa"""
        messagebox.showinfo(
            'About MrNotepad',
            'MrNotepad\nVersion 1.0\nA simple text editor\nBuilt with Python and Tkinter'
        )