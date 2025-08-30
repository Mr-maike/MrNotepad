# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk
from tkinter import ttk

class TestTabManager(unittest.TestCase):
    
    def setUp(self):
        """Configuração antes de cada teste - CORRIGIDO"""
        # Mock da aplicação principal
        self.mock_app = Mock()
        
        # Mock do root do Tkinter para evitar problemas com event loop
        self.mock_root = Mock()
        self.mock_app.root = self.mock_root
        
        # Mock do notebook
        self.mock_notebook = Mock()
        
        # Patch do ttk.Notebook durante os testes
        self.notebook_patcher = patch('core.tab_manager.ttk.Notebook')
        self.mock_notebook_class = self.notebook_patcher.start()
        self.mock_notebook_class.return_value = self.mock_notebook
        
        # Configura comportamento do mock notebook
        self.mock_notebook.index.return_value = 0
        self.mock_notebook.select.return_value = "tab1"
        
        # Importa após o patch
        from core.tab_manager import TabManager
        self.tab_manager = TabManager(self.mock_app)
        
        # Configura tabs mockadas
        self.tab_manager.tabs = {
            "tab1": {
                'frame': Mock(),
                'text_area': Mock(),
                'scrollbar': Mock(),
                'filename': None,
                'modified': False
            }
        }
        self.tab_manager.current_tab = "tab1"
    
    def tearDown(self):
        """Limpeza após cada teste"""
        self.notebook_patcher.stop()
    
    def test_tab_creation(self):
        """Testa criação de abas - CORRIGIDO"""
        initial_tab_count = len(self.tab_manager.tabs)
        
        # Configura o mock para retornar um novo tab_id
        self.mock_notebook.add.return_value = "tab2"
        
        # Adiciona nova aba
        tab_id = self.tab_manager.add_new_tab()
        
        # Verifica se o método add foi chamado
        self.mock_notebook.add.assert_called_once()
        
        # Verifica se a tab foi adicionada ao dicionário
        self.assertEqual(len(self.tab_manager.tabs), initial_tab_count + 1)
        self.assertIn("tab2", self.tab_manager.tabs)
    
    def test_tab_title_update(self):
        """Testa atualização de título das abas - CORRIGIDO"""
        tab_id = "tab1"
        
        # Configura o mock do notebook.tab
        self.mock_notebook.tab.return_value = None
        
        # Atualiza título
        self.tab_manager.update_tab_title(tab_id, "teste.txt", True)
        
        # Verifica se o método tab foi chamado corretamente
        self.mock_notebook.tab.assert_called_once_with(tab_id, text="teste.txt*")
        
        # Verifica se os dados da tab foram atualizados
        tab_data = self.tab_manager.tabs[tab_id]
        self.assertEqual(tab_data['filename'], "teste.txt")
        self.assertTrue(tab_data['modified'])
    
    @patch('core.tab_manager.messagebox.askyesnocancel')
    def test_tab_closing(self, mock_messagebox):
        """Testa fechamento de abas - CORRIGIDO"""
        mock_messagebox.return_value = True  # Simula "Yes"
        
        initial_tab_count = len(self.tab_manager.tabs)
        tab_id = "tab1"
        
        # Configura o mock do forget
        self.mock_notebook.forget.return_value = None
        
        self.tab_manager.close_tab(tab_id)
        
        # Verifica se o forget foi chamado
        self.mock_notebook.forget.assert_called_once_with(tab_id)
        
        # Verifica se a tab foi removida
        self.assertEqual(len(self.tab_manager.tabs), initial_tab_count - 1)
        self.assertNotIn(tab_id, self.tab_manager.tabs)
    
    def test_get_current_tab(self):
        """Testa obtenção da aba atual"""
        current_tab = self.tab_manager.get_current_tab()
        self.assertEqual(current_tab, self.tab_manager.tabs["tab1"])
    
    def test_get_current_text_area(self):
        """Testa obtenção da área de texto atual"""
        text_area = self.tab_manager.get_current_text_area()
        self.assertEqual(text_area, self.tab_manager.tabs["tab1"]['text_area'])
    
    @patch('core.tab_manager.os.path.basename')
    def test_update_display_with_filename(self, mock_basename):
        """Testa atualização do display com filename"""
        mock_basename.return_value = "teste.txt"
        
        # Configura tab com filename
        self.tab_manager.tabs["tab1"]['filename'] = "/path/to/teste.txt"
        self.tab_manager.tabs["tab1"]['modified'] = True
        
        self.tab_manager.update_display()
        
        # Verifica se o título foi atualizado
        self.mock_root.title.assert_called_once_with("teste.txt* - MrNotepad")
    
    def test_update_display_without_filename(self):
        """Testa atualização do display sem filename"""
        self.tab_manager.update_display()
        
        # Verifica se o título foi atualizado
        self.mock_root.title.assert_called_once_with("Untitled - MrNotepad")

if __name__ == '__main__':
    unittest.main()