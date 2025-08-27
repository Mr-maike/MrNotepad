# -*- coding: utf-8 -*-
import os
import tkinter as tk
from tkinter import filedialog, messagebox

class FileOperations:
    def __init__(self, app):
        self.app = app
        self.filename = None
        self.is_modified = False
        
    def set_modified(self, modified):
        #Define o estado de modificação do arquivo"""
        self.is_modified = modified
        self._update_display()
        
    def _update_display(self):
        #Atualiza a exibição com base no estado atual - CORRIGIDO"""
        name = os.path.basename(self.filename) if self.filename else 'Untitled'
        
        # CORREÇÃO: Usar o TabManager para atualizar o título
        current_tab = self.app.tab_manager.current_tab
        if current_tab:
            # Atualiza a aba atual
            self.app.tab_manager.update_tab_title(current_tab, self.filename, self.is_modified)
        else:
            # Fallback: atualiza o título da janela diretamente
            if self.is_modified:
                name += '*'
            self.app.root.title(f'{name} - MrNotepad')
            
    def new_file(self):
        #Cria um novo arquivo
        if self._check_save():
            # CORREÇÃO: Usar o TabManager para criar nova aba
            self.app.tab_manager.add_new_tab()
            self.filename = None
            self.is_modified = False
            self._update_display()
            self.app.update_status('New file created')
            
    def open_file(self):
        #Abre um arquivo existente
        if self._check_save():
            filename = filedialog.askopenfilename(
                defaultextension='.txt',
                filetypes=[
                    ('Text Files', '*.txt'),
                    ('Python Files', '*.py'),
                    ('HTML Files', '*.html'),
                    ('CSS Files', '*.css'),
                    ('JavaScript Files', '*.js'),
                    ('All Files', '*.*')
                ]
            )
            
            if filename:
                self._load_file(filename)
                
    def _load_file(self, filename):
        #Carrega o conteúdo de um arquivo - CORRIGIDO
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
            # CORREÇÃO: Usar o TabManager para criar aba com conteúdo
            tab_id = self.app.tab_manager.add_new_tab(filename, content)
            
            # Atualiza o filename e estado
            self.filename = filename
            self.is_modified = False
            
            # Atualiza a aba
            self.app.tab_manager.update_tab_title(tab_id, filename, False)
            self.app.update_status(f'Opened: {os.path.basename(filename)}')
            
        except UnicodeDecodeError:
            # Tenta abrir com encoding diferente
            try:
                with open(filename, 'r', encoding='latin-1') as file:
                    content = file.read()
                
                # CORREÇÃO: Usar o TabManager
                tab_id = self.app.tab_manager.add_new_tab(filename, content)
                
                self.filename = filename
                self.is_modified = False
                self.app.tab_manager.update_tab_title(tab_id, filename, False)
                self.app.update_status(f'Opened: {os.path.basename(filename)}')
            except Exception as e:
                messagebox.showerror('Error', f'Could not open file: {e}')
                
        except Exception as e:
            messagebox.showerror('Error', f'Could not open file: {e}')
            
    def save_file(self):
        #Salva o arquivo atual - CORRIGIDO
        # CORREÇÃO: Obter filename da aba atual
        current_tab = self.app.tab_manager.get_current_tab()
        if current_tab and current_tab['filename']:
            self.filename = current_tab['filename']
            self._save_to_file(self.filename)
        else:
            self.save_as()
            
    def save_as(self):
        #Salva o arquivo com um novo nome - CORRIGIDO"""
        filename = filedialog.asksaveasfilename(
            initialfile='Untitled.txt',
            defaultextension='.txt',
            filetypes=[
                ('Text Files', '*.txt'),
                ('Python Files', '*.py'),
                ('HTML Files', '*.html'),
                ('CSS Files', '*.css'),
                ('JavaScript Files', '*.js'),
                ('All Files', '*.*')
            ]
        )
        
        if filename:
            self._save_to_file(filename)
            # CORREÇÃO: Atualizar a aba atual com o novo filename
            current_tab_id = self.app.tab_manager.current_tab
            if current_tab_id:
                self.app.tab_manager.update_tab_title(current_tab_id, filename, False)
            
    def _save_to_file(self, filename):
        #Salva o conteúdo no arquivo especificado - CORRIGIDO
        try:
            # CORREÇÃO: Obter conteúdo da aba atual
            text_area = self.app.tab_manager.get_current_text_area()
            if text_area:
                content = text_area.get(1.0, tk.END)
                
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # Atualiza o estado
                self.filename = filename
                self.is_modified = False
                
                # CORREÇÃO: Atualizar a aba atual
                current_tab_id = self.app.tab_manager.current_tab
                if current_tab_id:
                    self.app.tab_manager.update_tab_title(current_tab_id, filename, False)
                
                self.app.update_status(f'Saved: {os.path.basename(filename)}')
                
        except Exception as e:
            messagebox.showerror('Error', f'Could not save file: {e}')
            
    def _check_save(self):
        #Verifica se deve salvar antes de proceder"""
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
        #Fecha o programa
        if self._check_save():
            self.app.root.quit()
