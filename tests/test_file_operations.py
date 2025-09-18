# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch
import tempfile
import os

class TestFileOperations(unittest.TestCase):

    def setUp(self):
        """Configuração antes de cada teste"""
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

        # Controle de arquivos temporários criados
        self.temp_files = []

    def tearDown(self):
        """Remove arquivos temporários criados durante os testes"""
        for f in self.temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def _create_temp_file(self, content="conteúdo de teste"):
        """Helper para criar arquivo temporário e registrar para limpeza"""
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
        with open(tmp.name, 'w', encoding='utf-8') as f:
            f.write(content)
        self.temp_files.append(tmp.name)
        return tmp.name

    def test_new_file_creation(self):
        """Testa criação de novo arquivo"""
        with patch.object(self.file_ops, '_check_save', return_value=True):
            self.file_ops.new_file()
            
            self.mock_tab_manager.add_new_tab.assert_called_once()
            self.assertIsNone(self.file_ops.filename)
            self.assertFalse(self.file_ops.is_modified)

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_save_as_with_filename(self, mock_asksaveasfilename):
        """Testa salvamento com nome de arquivo"""
        test_filename = self._create_temp_file("")
        mock_asksaveasfilename.return_value = test_filename
        self.mock_text_area.get.return_value = "conteúdo de teste"
        
        self.file_ops.save_as()
        
        self.assertTrue(os.path.exists(test_filename))
        with open(test_filename, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), "conteúdo de teste")
        
        self.mock_tab_manager.update_tab_title.assert_any_call("tab1", test_filename, False)

    @patch('tkinter.filedialog.asksaveasfilename', return_value='')
    def test_save_as_cancelled(self, mock_asksaveasfilename):
        """Testa cancelamento do Save As"""
        self.mock_text_area.get.return_value = "texto qualquer"
        result = self.file_ops.save_as()
        
        self.assertIsNone(result)
        self.mock_tab_manager.update_tab_title.assert_not_called()

    @patch('tkinter.filedialog.askopenfilename')
    def test_file_loading(self, mock_askopenfilename):
        """Testa carregamento de arquivo"""
        test_filename = self._create_temp_file("conteúdo de teste")
        mock_askopenfilename.return_value = test_filename
        
        with patch.object(self.file_ops, '_check_save', return_value=True):
            self.file_ops.open_file()
            
            self.mock_tab_manager.add_new_tab.assert_called_once_with(test_filename, "conteúdo de teste")
            self.mock_tab_manager.update_tab_title.assert_called_once()

    def test_save_file_scenarios(self):
        """Testa salvamento com e sem filename"""
        scenarios = [
            {"desc": "com filename existente", "tab_data": {"filename": "test.txt"}, "expect_save_as": False},
            {"desc": "sem filename", "tab_data": {"filename": None}, "expect_save_as": True},
        ]

        for sc in scenarios:
            with self.subTest(sc["desc"]):
                self.mock_tab_manager.get_current_tab.return_value = sc["tab_data"]

                if sc["expect_save_as"]:
                    with patch.object(self.file_ops, 'save_as') as mock_save_as:
                        self.file_ops.save_file()
                        mock_save_as.assert_called_once()
                else:
                    with patch.object(self.file_ops, '_save_to_file') as mock_save:
                        self.file_ops.save_file()
                        mock_save.assert_called_once_with("test.txt")

    def test_save_file_with_error(self):
        """Testa erro ao salvar arquivo existente"""
        self.mock_tab_manager.get_current_tab.return_value = {"filename": "test.txt"}
        
        with patch.object(self.file_ops, '_save_to_file', side_effect=PermissionError("sem permissão")):
            with self.assertRaises(PermissionError):
                self.file_ops.save_file()

    def test__save_to_file_direct(self):
        """Testa método interno _save_to_file diretamente"""
        test_filename = self._create_temp_file("")
        self.mock_text_area.get.return_value = "conteúdo direto"
        
        self.file_ops._save_to_file(test_filename)
        
        with open(test_filename, 'r', encoding='utf-8') as f:
            self.assertEqual(f.read(), "conteúdo direto")


if __name__ == '__main__':
    unittest.main()
