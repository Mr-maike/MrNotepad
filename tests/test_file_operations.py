# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os

class TestFileOperations(unittest.TestCase):
    
    def setUp(self):
        """Configuração antes de cada teste - CORRIGIDO"""
        self.mock_app = Mock()
        
        # Mock do tab_manager
        self.mock_tab_manager = Mock()
        self.mock_app.tab_manager = self.mock_tab_manager
        
        # Mock da text area
        self.mock_text_area = Mock()
        self.mock_tab_manager.get_current_text_area.return_value = self.mock_text_area
        self.mock_tab_manager.current_tab = "tab1"
        
        from core.file_operations import FileOperations
        self.file_ops = FileOperations(self.mock_app)
        
    def test_new_file_creation(self):
        """Testa criação de novo arquivo - CORRIGIDO"""
        with patch.object(self.file_ops, '_check_save', return_value=True):
            self.file_ops.new_file()
            
            # Verifica se add_new_tab foi chamado
            self.mock_tab_manager.add_new_tab.assert_called_once()
            
            # Verifica se o estado foi resetado
            self.assertIsNone(self.file_ops.filename)
            self.assertFalse(self.file_ops.is_modified)
    
    @patch('tkinter.filedialog.asksaveasfilename')
    def test_save_as_with_filename(self, mock_asksaveasfilename):
        """Testa salvamento com nome de arquivo - CORRIGIDO"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            test_filename = tmp.name
            
        try:
            mock_asksaveasfilename.return_value = test_filename
            
            # Mock do conteúdo da text area
            self.mock_text_area.get.return_value = "conteúdo de teste"
            
            self.file_ops.save_as()
            
            # Verifica se o arquivo foi criado
            self.assertTrue(os.path.exists(test_filename))
            
            # Verifica o conteúdo
            with open(test_filename, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertEqual(content, "conteúdo de teste")
            
            # Verifica se update_tab_title foi chamado
            self.mock_tab_manager.update_tab_title.assert_called_once_with("tab1", test_filename, False)
            
        finally:
            # Limpeza
            if os.path.exists(test_filename):
                os.unlink(test_filename)
    
    @patch('tkinter.filedialog.askopenfilename')
    def test_file_loading(self, mock_askopenfilename):
        """Testa carregamento de arquivo - CORRIGIDO"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
            test_filename = tmp.name
            with open(test_filename, 'w', encoding='utf-8') as f:
                f.write("conteúdo de teste")
                
        try:
            mock_askopenfilename.return_value = test_filename
            
            with patch.object(self.file_ops, '_check_save', return_value=True):
                self.file_ops.open_file()
                
                # Verifica se add_new_tab foi chamado com o conteúdo
                self.mock_tab_manager.add_new_tab.assert_called_once_with(test_filename, "conteúdo de teste")
                
                # Verifica se update_tab_title foi chamado
                self.mock_tab_manager.update_tab_title.assert_called_once()
                
        finally:
            if os.path.exists(test_filename):
                os.unlink(test_filename)
    
    def test_save_file_existing_filename(self):
        """Testa salvamento com filename existente - CORRIGIDO"""
        # Configura tab atual com filename
        mock_tab_data = {'filename': 'test.txt'}
        self.mock_tab_manager.get_current_tab.return_value = mock_tab_data
        
        # Mock do método de salvamento
        with patch.object(self.file_ops, '_save_to_file') as mock_save:
            self.file_ops.save_file()
            
            # Verifica se _save_to_file foi chamado
            mock_save.assert_called_once_with('test.txt')
    
    def test_save_file_no_filename(self):
        """Testa salvamento sem filename - CORRIGIDO"""
        # Configura tab atual sem filename
        mock_tab_data = {'filename': None}
        self.mock_tab_manager.get_current_tab.return_value = mock_tab_data
        
        # Mock do save_as
        with patch.object(self.file_ops, 'save_as') as mock_save_as:
            self.file_ops.save_file()
            
            # Verifica se save_as foi chamado
            mock_save_as.assert_called_once()

if __name__ == '__main__':
    unittest.main()