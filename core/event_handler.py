# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

class EventHandler:
    def __init__(self, app):
        self.app = app
        self.setup_handlers()
        
    def setup_handlers(self):
        #Configura e registra todos os handlers
        # Registra handlers no tab_manager
        self.app.tab_manager.add_bind_handler(self.bind_basic_events)
        self.app.tab_manager.add_bind_handler(self.bind_navigation_events)
        self.app.tab_manager.add_bind_handler(self.bind_edit_events)
        self.app.tab_manager.add_bind_handler(self.bind_file_events)
        
        # Configura eventos globais
        self.bind_global_events()
        
    def bind_global_events(self):
        #Eventos globais da aplicação
        # Bind para o notebook
        self.app.tab_manager.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Bind global de teclado
        self.app.root.bind('<Control-N>', lambda e: self.app.file_operations.new_file())
        self.app.root.bind('<Control-n>', lambda e: self.app.file_operations.new_file())
        self.app.root.bind('<Control-O>', lambda e: self.app.file_operations.open_file())
        self.app.root.bind('<Control-o>', lambda e: self.app.file_operations.open_file())
        
    def bind_basic_events(self, text_widget):
        #Eventos básicos de texto
        # Modificação do texto
        text_widget.bind('<<Modified>>', self.on_text_modified)
        
        # Movimento do cursor
        text_widget.bind('<KeyRelease>', self.on_cursor_move)
        text_widget.bind('<ButtonRelease-1>', self.on_cursor_move)
        text_widget.bind('<B1-Motion>', self.on_cursor_move)
        
    def bind_navigation_events(self, text_widget):
        #Eventos de navegação
        # Scroll
        text_widget.bind('<MouseWheel>', self.on_scroll)
        text_widget.bind('<Button-4>', self.on_scroll)
        text_widget.bind('<Button-5>', self.on_scroll)
        
    def bind_edit_events(self, text_widget):
        """Eventos de edição"""
        # Atalhos de edição
        text_widget.bind('<Control-z>', lambda e: text_widget.edit_undo())
        text_widget.bind('<Control-y>', lambda e: text_widget.edit_redo())
        text_widget.bind('<Control-a>', self.select_all)
        
        # Menu de contexto
        text_widget.bind('<Button-3>', self.on_text_right_click)
        
    def bind_file_events(self, text_widget):
        #Eventos de arquivo
        # Salvamento
        text_widget.bind('<Control-s>', lambda e: self.app.file_operations.save_file())
        text_widget.bind('<Control-S>', lambda e: self.app.file_operations.save_as())
        
    def on_text_modified(self, event):
        #Quando o texto é modificado - CORRIGIDO
        text_widget = event.widget
        
        try:
            # Encontra a aba correspondente
            for tab_id, tab_data in self.app.tab_manager.tabs.items():
                if tab_data['text_area'] == text_widget:
                    tab_data['modified'] = True
                    
                    # CORREÇÃO: Verifica se o tab_id é válido antes de atualizar
                    if tab_id in self.app.tab_manager.tabs:
                        self.app.tab_manager.update_tab_title(tab_id, tab_data['filename'], True)
                    
                    # Reseta o flag de modificação
                    text_widget.edit_modified(False)
                    break
        except Exception as e:
            # Em caso de erro, apenas ignora e reseta o flag
            text_widget.edit_modified(False)
    
    def on_cursor_move(self, event):
        #Quando o cursor se move
        # Usa after para evitar atualizações muito frequentes
        self.app.root.after(100, self.app.tab_manager.update_status_bar)
        
    def on_scroll(self, event):
        #Evento de scroll
        # Atualiza status após scroll
        self.app.root.after(100, self.app.tab_manager.update_status_bar)
        
    def on_tab_changed(self, event):
        """Quando muda de aba"""
        # Atualiza a barra de status quando muda de aba
        self.app.tab_manager.update_status_bar()
        
    def select_all(self, event):
        #Seleciona todo o texto"""
        try:
            event.widget.tag_add(tk.SEL, "1.0", tk.END)
            event.widget.mark_set(tk.INSERT, "1.0")
            event.widget.see(tk.INSERT)
            return "break"
        except:
            return "break"
        
    def on_text_right_click(self, event):
        #Menu de contexto no texto
        text_widget = event.widget
        
        try:
            # Cria menu de contexto
            menu = tk.Menu(self.app.root, tearoff=0)
            menu.add_command(label="Undo", command=text_widget.edit_undo)
            menu.add_command(label="Redo", command=text_widget.edit_redo)
            menu.add_separator()
            menu.add_command(label="Cut", command=lambda: text_widget.event_generate('<<Cut>>'))
            menu.add_command(label="Copy", command=lambda: text_widget.event_generate('<<Copy>>'))
            menu.add_command(label="Paste", command=lambda: text_widget.event_generate('<<Paste>>'))
            menu.add_separator()
            menu.add_command(label="Select All", command=lambda: self.select_all_event(text_widget))
            
            # Mostra menu na posição do mouse
            menu.tk_popup(event.x_root, event.y_root)
        except:
            pass
        
    def select_all_event(self, text_widget):
        #Seleciona todo o texto para o menu de contexto
        try:
            text_widget.tag_add(tk.SEL, "1.0", tk.END)
            text_widget.mark_set(tk.INSERT, "1.0")
            text_widget.see(tk.INSERT)
        except:
            pass
