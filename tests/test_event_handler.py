# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, MagicMock
import sys
import os

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.event_handler import EventHandler

class TestEventHandler(unittest.TestCase):
    
    def setUp(self):
        self.mock_app = Mock()
        self.event_handler = EventHandler(self.mock_app)
    
    def test_text_modified_event(self):
        """Testa evento de modificação de texto"""
        # Mock do widget de texto
        mock_text_widget = Mock()
        mock_event = Mock()
        mock_event.widget = mock_text_widget
        
        # Mock do tab_manager
        mock_tab_data = {'text_area': mock_text_widget, 'filename': 'test.txt', 'modified': False}
        self.mock_app.tab_manager.tabs = {'tab1': mock_tab_data}
        self.mock_app.tab_manager.update_tab_title = Mock()
        
        self.event_handler.on_text_modified(mock_event)
        
        self.assertTrue(mock_tab_data['modified'])
        mock_text_widget.edit_modified.assert_called_with(False)
        self.mock_app.tab_manager.update_tab_title.assert_called_once()
    
    def test_keyboard_shortcuts(self):
        """Testa bindings de teclado"""
        # Mock do widget de texto
        mock_text_widget = Mock()
        
        # Testa bind de atalhos
        self.event_handler.bind_file_events(mock_text_widget)
        
        # Verifica se os binds foram criados
        self.assertGreaterEqual(mock_text_widget.bind.call_count, 2)
    
    def test_cursor_move_event(self):
        """Testa evento de movimento do cursor"""
        mock_event = Mock()
        
        # Mock do after
        self.mock_app.root.after = Mock()
        
        self.event_handler.on_cursor_move(mock_event)
        
        self.mock_app.root.after.assert_called_once_with(100, self.mock_app.tab_manager.update_status_bar)

if __name__ == '__main__':
    unittest.main()