# -*- coding: utf-8 -*-
import tkinter as tk

class EventHandler:
    def __init__(self, app):
        self.app = app
        self.bind_events()
        
    def bind_events(self):
        """Configura todos os eventos"""
        self._bind_keyboard_events()
        self._bind_text_events()
        self._bind_window_events()
        
    def _bind_keyboard_events(self):
        """Configura eventos de teclado"""
        # Atalhos de arquivo
        self.app.root.bind('<Control-n>', lambda e: self.app.file_operations.new_file())
        self.app.root.bind('<Control-o>', lambda e: self.app.file_operations.open_file())
        self.app.root.bind('<Control-s>', lambda e: self.app.file_operations.save_file())
        self.app.root.bind('<Control-Shift-S>', lambda e: self.app.file_operations.save_as())
        
        # Atalhos de edição
        self.app.root.bind('<Control-z>', lambda e: self.app.menu_manager._undo())
        self.app.root.bind('<Control-y>', lambda e: self.app.menu_manager._redo())
        self.app.root.bind('<Control-x>', lambda e: self.app.menu_manager._cut())
        self.app.root.bind('<Control-c>', lambda e: self.app.menu_manager._copy())
        self.app.root.bind('<Control-v>', lambda e: self.app.menu_manager._paste())
        self.app.root.bind('<Control-a>', lambda e: self.app.menu_manager._select_all())
        
    def _bind_text_events(self):
        """Configura eventos do texto"""
        self.app.text_editor.text_area.bind('<<Modified>>', self._on_text_modified)
        
    def _bind_window_events(self):
        """Configura eventos da janela"""
        self.app.root.protocol("WM_DELETE_WINDOW", self.app.file_operations.exit_program)
        
    def _on_text_modified(self, event=None):
        """Handler para quando o texto é modificado"""
        if self.app.text_editor.text_area.edit_modified():
            self.app.file_operations.set_modified(True)
            self.app.text_editor.text_area.edit_modified(False)