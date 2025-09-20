# -*- coding: utf-8 -*-
import tkinter as tk
from .tab_manager import TabManager
from .file_operations import FileOperations
from .menu_manager import MenuManager
from .event_handler import EventHandler
from .side_bar import Sidebar  # NOVO

class MrNotepad:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Inicializa os componentes na ordem correta
        self.sidebar = Sidebar(self)  # NOVO: Sidebar primeiro
        self.tab_manager = TabManager(self)
        self.file_operations = FileOperations(self)
        self.menu_manager = MenuManager(self)
        self.event_handler = EventHandler(self)
        self.status_bar = 'Waiting for next action...'  # Placeholder para status bar
        
    def setup_window(self):
        """Configura a janela principal - ATUALIZADO"""
        self.root.title('Untitled - MrNotepad')
        self.root.geometry('1000x600')  # Largura maior para acomodar sidebar
        self.root.minsize(800, 500)
        
        # Configura peso das colunas (sidebar + editor)
        self.root.grid_columnconfigure(0, weight=0)  # Sidebar (largura fixa)
        self.root.grid_columnconfigure(1, weight=1)  # Editor (expansível)
        self.root.grid_rowconfigure(0, weight=1)

    def update_status(self, message):
        # Atualiza a mensagem da barra de status do app
        self.status_bar=message
