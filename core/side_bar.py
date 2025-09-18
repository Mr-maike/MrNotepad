# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import os
from PIL import Image

class Sidebar:
    def __init__(self, app):
        self.app = app
        self.is_visible = True
        self.width = 250  # Largura padrão
        self.setup_sidebar()
        
    def setup_sidebar(self):
        """Configura a sidebar principal"""
        # Frame principal da sidebar
        self.sidebar_frame = ttk.Frame(self.app.root, width=self.width)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
        self.sidebar_frame.pack_propagate(False)  # Mantém a largura fixa
        
        # Botão de toggle (ocultar/mostrar)
        self.toggle_button = ttk.Button(
            self.sidebar_frame, 
            text="◀", 
            width=3,
            command=self.toggle_sidebar
        )
        self.toggle_button.pack(side=tk.TOP, fill=tk.X, pady=2)
        
        # Notebook para múltiplas abas na sidebar
        self.sidebar_notebook = ttk.Notebook(self.sidebar_frame)
        self.sidebar_notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Aba do explorador de arquivos
        self.file_explorer_frame = ttk.Frame(self.sidebar_notebook)
        self.sidebar_notebook.add(self.file_explorer_frame, text="Explorador")
        
        # Aba de busca (futura implementação)
        self.search_frame = ttk.Frame(self.sidebar_notebook)
        self.sidebar_notebook.add(self.search_frame, text="Buscar")
        
        # Aba de extensões (futura implementação)
        self.extensions_frame = ttk.Frame(self.sidebar_notebook)
        self.sidebar_notebook.add(self.extensions_frame, text="Extensões")
        
        # Inicializa o explorador de arquivos
        self.setup_file_explorer()
        
    def setup_file_explorer(self):
        """Configura o explorador de arquivos"""
        # Frame para controles
        control_frame = ttk.Frame(self.file_explorer_frame)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Campo de caminho
        self.path_var = tk.StringVar(value=os.getcwd())
        self.path_entry = ttk.Entry(control_frame, textvariable=self.path_var)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Botão de atualizar
        self.refresh_btn = ttk.Button(
            control_frame, 
            text="↻", 
            width=3,
            command=self.refresh_explorer
        )
        self.refresh_btn.pack(side=tk.RIGHT)
        
        # Botão de navegar para pasta anterior
        self.back_btn = ttk.Button(
            control_frame, 
            text="←", 
            width=3,
            command=self.navigate_back
        )
        self.back_btn.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Treeview para mostrar arquivos e pastas
        self.tree = ttk.Treeview(
            self.file_explorer_frame, 
            show='tree', 
            selectmode='browse'
        )
        
        # Scrollbar
        self.tree_scroll = ttk.Scrollbar(
            self.file_explorer_frame, 
            orient=tk.VERTICAL, 
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        self.path_entry.bind('<Return>', self.on_path_entry_return)
        
        # Carrega o diretório atual
        self.load_directory(os.getcwd())
        
    def load_directory(self, path):
        """Carrega um diretório no treeview"""
        # Limpa o treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Adiciona o diretório atual
            self.tree.heading('#0', text=f" {os.path.basename(path)}")
            
            # Adiciona pastas primeiro
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    self.tree.insert(
                        '', 'end', 
                        text=f" 📁 {item}", 
                        values=[item_path],
                        open=False
                    )
            
            # Adiciona arquivos depois
            for item in sorted(os.listdir(path)):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    # Ícone baseado na extensão
                    icon = self.get_file_icon(item)
                    self.tree.insert(
                        '', 'end', 
                        text=f" {icon} {item}", 
                        values=[item_path],
                        open=False
                    )
                    
        except PermissionError:
            self.tree.heading('#0', text=" Acesso negado")
        except Exception as e:
            self.tree.heading('#0', text=f" Erro: {str(e)}")
    
    def get_file_icon(self, filename):
        """Retorna emoji baseado na extensão do arquivo"""
        ext = os.path.splitext(filename)[1].lower()
        
        icon_map = {
            '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨',
            '.txt': '📄', '.md': '📝', '.json': '🔧', '.xml': '📋',
            '.csv': '📊', '.sql': '🗃️', '.java': '☕', '.cpp': '⚙️',
            '.c': '🔧', '.rs': '🦀', '.go': '🐹', '.php': '🐘',
            '.rb': '💎', '.ts': '📘', '.vue': '🟢', '.react': '⚛️',
            '.jpg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
            '.mp3': '🎵', '.mp4': '🎬', '.pdf': '📕', '.doc': '📘',
            '.docx': '📘', '.xls': '📗', '.xlsx': '📗', '.zip': '📦',
            '.rar': '📦', '.7z': '📦'
        }
        
        return icon_map.get(ext, '📄')
    
    def on_tree_select(self, event):
        """Quando um item é selecionado"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            self.path_var.set(item['values'][0])
    
    def on_tree_double_click(self, event):
        """Quando um item é clicado duas vezes"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            item_path = item['values'][0]
            
            if os.path.isdir(item_path):
                # Navega para a pasta
                self.load_directory(item_path)
                self.path_var.set(item_path)
            elif os.path.isfile(item_path):
                # Abre o arquivo
                self.app.file_operations._load_file(item_path)
    
    def on_path_entry_return(self, event):
        """Quando Enter é pressionado no campo de caminho"""
        path = self.path_var.get()
        if os.path.exists(path):
            if os.path.isdir(path):
                self.load_directory(path)
            else:
                self.app.file_operations._load_file(path)
    
    def refresh_explorer(self):
        """Atualiza o explorador"""
        current_path = self.path_var.get()
        if os.path.exists(current_path):
            self.load_directory(current_path)
    
    def navigate_back(self):
        """Navega para a pasta anterior"""
        current_path = self.path_var.get()
        parent_path = os.path.dirname(current_path)
        
        if os.path.exists(parent_path):
            self.load_directory(parent_path)
            self.path_var.set(parent_path)
    
    def toggle_sidebar(self):
        """Alterna a visibilidade da sidebar"""
        self.is_visible = not self.is_visible
        
        if self.is_visible:
            self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 2))
            self.toggle_button.config(text="◀")
        else:
            self.sidebar_frame.pack_forget()
            self.toggle_button.config(text="▶")
    
    def update_sidebar_width(self, width):
        """Atualiza a largura da sidebar"""
        self.width = width
        self.sidebar_frame.config(width=width)