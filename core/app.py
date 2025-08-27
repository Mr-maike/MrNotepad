# -*- coding: utf-8 -*-
import tkinter as tk
from .tab_manager import TabManager
from .file_operations import FileOperations
from .menu_manager import MenuManager
from .event_handler import EventHandler

class MrNotepad:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Inicializa os componentes na ordem correta
        self.tab_manager = TabManager(self)
        self.file_operations = FileOperations(self)
        self.menu_manager = MenuManager(self)
        self.event_handler = EventHandler(self)
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title('Untitled - MrNotepad')
        self.root.geometry('800x600')
        self.root.minsize(600, 500)
        
    def update_status(self, message):
        #Atualiza a barra de status
        if hasattr(self.tab_manager, 'status_bar'):
            self.tab_manager.status_bar.config(text=message)
        
    def get_text_content(self):
        #Retorna o conteúdo do texto atual
        text_area = self.tab_manager.get_current_text_area()
        return text_area.get(1.0, tk.END) if text_area else ""
        
    def set_text_content(self, content):
        #Define o conteúdo do texto atual
        text_area = self.tab_manager.get_current_text_area()
        if text_area:
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, content)
        
    def clear_text(self):
        #Limpa o conteúdo do texto atual
        text_area = self.tab_manager.get_current_text_area()
        if text_area:
            text_area.delete(1.0, tk.END)
            
    def new_tab_with_content(self, filename=None, content=None):
        #Cria uma nova aba com conteúdo
        return self.tab_manager.add_new_tab(filename, content)
