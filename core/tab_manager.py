# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import os

class TabManager:
    def __init__(self, app):
        self.app = app
        self.tabs = {}
        self.current_tab = None
        self.text_bind_handlers = []
        self.setup_tab_widget()
        
    def setup_tab_widget(self):
        """Configura o widget de abas"""
        # Style moderno para as abas
        style = ttk.Style()
        style.configure("TNotebook", tabposition='n')
        style.configure("TNotebook.Tab", padding=[10, 4], font=('Segoe UI', 9))
        
        # Widget de abas
        self.notebook = ttk.Notebook(self.app.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind events do notebook
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        self.notebook.bind("<Button-2>", self.on_middle_click)
        self.notebook.bind("<Button-3>", self.on_right_click)
        
        # Barra de status
        self.status_bar = tk.Label(
            self.app.root, 
            text='Ready', 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            padx=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Cria a primeira aba
        self.add_new_tab()
        
    def add_bind_handler(self, handler):
        """Adiciona um handler para binds de texto"""
        self.text_bind_handlers.append(handler)
        
        # Aplica o handler às abas existentes
        for tab_data in self.tabs.values():
            handler(tab_data['text_area'])
            
    def add_new_tab(self, filename=None, content=None):
        """Adiciona uma nova aba"""
        # Frame para a aba
        tab_frame = ttk.Frame(self.notebook)
        
        # Área de texto com scrollbar
        text_area = tk.Text(
            tab_frame, 
            wrap=tk.WORD, 
            undo=True,
            font=('Consolas', 11),
            padx=10,
            pady=10
        )
        
        scrollbar = ttk.Scrollbar(tab_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insere conteúdo se fornecido
        if content:
            text_area.insert(1.0, content)
        
        # Nome da aba
        tab_name = os.path.basename(filename) if filename else "Untitled"
        tab_id = self.notebook.add(tab_frame, text=tab_name)
        
        # Configurações da aba
        self.tabs[tab_id] = {
            'frame': tab_frame,
            'text_area': text_area,
            'scrollbar': scrollbar,
            'filename': filename,
            'modified': False
        }
        
        # Aplica todos os handlers de bind à nova área de texto
        for handler in self.text_bind_handlers:
            handler(text_area)
        
        # Define como aba atual
        self.notebook.select(tab_id)
        self.current_tab = tab_id
        
        # Foca na área de texto
        text_area.focus_set()
        text_area.mark_set(tk.INSERT, '1.0')
        
        # Atualiza a barra de status
        self.update_status_bar()
        
        return tab_id
        
    def get_current_tab(self):
        """Retorna a aba atual"""
        return self.tabs.get(self.current_tab)
        
    def get_current_text_area(self):
        """Retorna a área de texto atual"""
        tab = self.get_current_tab()
        return tab['text_area'] if tab else None
        
    def on_tab_changed(self, event):
        """Evento quando muda de aba"""
        selected_tab = self.notebook.select()
        if selected_tab:
            self.current_tab = selected_tab
            self.update_display()
                
    def update_display(self):
        """Atualiza título e status da aba atual"""
        tab_data = self.get_current_tab()
        if tab_data:
            # Atualiza título
            name = os.path.basename(tab_data['filename']) if tab_data['filename'] else 'Untitled'
            if tab_data['modified']:
                name += '*'
            self.app.root.title(f'{name} - MrNotepad')
            
            # Atualiza barra de status
            self.update_status_bar()
                
    def update_status_bar(self):
        """Atualiza a barra de status com informações do cursor"""
        tab_data = self.get_current_tab()
        if tab_data and tab_data['text_area']:
            text_area = tab_data['text_area']
            
            try:
                # Calcula linha e coluna
                cursor_position = text_area.index(tk.INSERT)
                line, column = cursor_position.split('.')
                
                # Conta linhas totais
                total_lines = int(text_area.index('end-1c').split('.')[0])
                
                # Status info
                status = f"Line: {line}, Column: {column} | Lines: {total_lines}"
                if tab_data['filename']:
                    status += f" | File: {os.path.basename(tab_data['filename'])}"
                if tab_data['modified']:
                    status += " | Modified"
                    
                self.status_bar.config(text=status)
            except Exception as e:
                # Em caso de erro, mostra mensagem simples
                self.status_bar.config(text="Ready")
            
    def update_tab_title(self, tab_id, filename=None, modified=False):
        """Atualiza o título de uma aba - CORRIGIDO"""
        if tab_id in self.tabs:
            self.tabs[tab_id]['filename'] = filename
            self.tabs[tab_id]['modified'] = modified
            
            name = os.path.basename(filename) if filename else "Untitled"
            if modified:
                name += "*"
            
            # CORREÇÃO: Usar o método correto para atualizar o texto da aba
            try:
                # Método 1: Usando a abordagem correta do ttk.Notebook
                self.notebook.tab(tab_id, text=name)
            except tk.TclError:
                # Método 2: Alternativa mais segura
                try:
                    # Tenta reconverter o tab_id para índice numérico
                    if isinstance(tab_id, str):
                        # Se for string, tenta converter para índice
                        tab_index = self.notebook.index(tab_id)
                        self.notebook.tab(tab_index, text=name)
                    else:
                        # Se já for numérico, usa diretamente
                        self.notebook.tab(tab_id, text=name)
                except:
                    # Método 3: Fallback - simplesmente ignora o erro
                    pass
            
            self.update_display()
    
    def on_middle_click(self, event):
        """Fecha aba com clique do meio"""
        try:
            tab_id = self.notebook.index(f"@{event.x},{event.y}")
            if tab_id >= 0:
                self.close_tab(tab_id)
        except:
            pass
            
    def on_right_click(self, event):
        """Menu de contexto para abas"""
        try:
            tab_id = self.notebook.index(f"@{event.x},{event.y}")
            if tab_id >= 0:
                menu = tk.Menu(self.app.root, tearoff=0)
                menu.add_command(label="Close", command=lambda: self.close_tab(tab_id))
                menu.add_command(label="Close Others", command=lambda: self.close_other_tabs(tab_id))
                menu.add_command(label="Close All", command=self.close_all_tabs)
                menu.tk_popup(event.x_root, event.y_root)
        except:
            pass
            
    def close_tab(self, tab_id=None):
        """Fecha uma aba"""
        if tab_id is None:
            tab_id = self.current_tab
            
        if tab_id in self.tabs:
            # Verifica se há modificações não salvas
            tab_data = self.tabs[tab_id]
            if tab_data['modified']:
                # TODO: Implementar lógica para perguntar se quer salvar
                pass
                
            # Remove a aba
            self.notebook.forget(tab_id)
            del self.tabs[tab_id]
            
            # Se não houver mais abas, cria uma nova
            if not self.tabs:
                self.add_new_tab()
            else:
                # Atualiza a barra de status
                self.update_status_bar()
                
    def close_other_tabs(self, keep_tab_id):
        """Fecha todas as outras abas"""
        for tab_id in list(self.tabs.keys()):
            if tab_id != keep_tab_id:
                self.close_tab(tab_id)
                
    def close_all_tabs(self):
        """Fecha todas as abas"""
        for tab_id in list(self.tabs.keys()):
            self.close_tab(tab_id)