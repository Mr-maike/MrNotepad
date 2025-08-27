# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import scrolledtext

class TextEditor:
    def __init__(self, app):
        self.app = app
        self.create_widgets()
        
    def create_widgets(self):
        #Cria os widgets do editor de texto"""
        # Frame principal
        self.main_frame = tk.Frame(self.app.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de texto com scrollbar
        self.text_area = scrolledtext.ScrolledText(
            self.main_frame, 
            wrap=tk.WORD, 
            undo=True,
            font=('Consolas', 11),
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Barra de status
        self.status_bar = tk.Label(
            self.app.root, 
            text='Ready', 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            padx=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def get_content(self):
        #Retorna o conteúdo do texto"""
        return self.text_area.get(1.0, tk.END)
        
    def set_content(self, content):
        #Define o conteúdo do texto"""
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(1.0, content)
        
    def clear_content(self):
        #Limpa o conteúdo do texto"""
        self.text_area.delete(1.0, tk.END)
        
    def update_status(self, message):
        #Atualiza a barra de status"""
        self.status_bar.config(text=message)
        
    def has_selection(self):
        #Verifica se há texto selecionado"""
        try:
            return bool(self.text_area.tag_ranges(tk.SEL))
        except:
            return False
