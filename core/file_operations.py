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
        """Define o estado de modificação do arquivo"""
        self.is_modified = modified
        self._update_display()
        
    def _update_display(self):
        """Atualiza a exibição com base no estado atual"""
        name = os.path.basename(self.filename) if self.filename else 'Untitled'
        self.app.update_title(name, self.is_modified)
        
    def new_file(self):
        """Cria um novo arquivo"""
        if self._check_save():
            self.app.clear_text()
            self.filename = None
            self.is_modified = False
            self._update_display()
            self.app.update_status('New file created')
            
    def open_file(self):
        """Abre um arquivo existente"""
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
        """Carrega o conteúdo de um arquivo"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
                
            self.app.set_text_content(content)
            self.filename = filename
            self.is_modified = False
            self._update_display()
            self.app.update_status(f'Opened: {os.path.basename(filename)}')
            
        except UnicodeDecodeError:
            # Tenta abrir com encoding diferente
            try:
                with open(filename, 'r', encoding='latin-1') as file:
                    content = file.read()
                self.app.set_text_content(content)
                self.filename = filename
                self.is_modified = False
                self._update_display()
                self.app.update_status(f'Opened: {os.path.basename(filename)}')
            except Exception as e:
                messagebox.showerror('Error', f'Could not open file: {e}')
                
        except Exception as e:
            messagebox.showerror('Error', f'Could not open file: {e}')
            
    def save_file(self):
        """Salva o arquivo atual"""
        if self.filename:
            self._save_to_file(self.filename)
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
                ('HTML Files', '*.html'),
                ('CSS Files', '*.css'),
                ('JavaScript Files', '*.js'),
                ('All Files', '*.*')
            ]
        )
        
        if filename:
            self._save_to_file(filename)
            self.filename = filename
            self._update_display()
            
    def _save_to_file(self, filename):
        """Salva o conteúdo no arquivo especificado"""
        try:
            content = self.app.get_text_content()
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(content)
                
            self.is_modified = False
            self._update_display()
            self.app.update_status(f'Saved: {os.path.basename(filename)}')
            
        except Exception as e:
            messagebox.showerror('Error', f'Could not save file: {e}')
            
    def _check_save(self):
        """Verifica se deve salvar antes de proceder"""
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
        if self._check_save():
            self.app.root.quit()