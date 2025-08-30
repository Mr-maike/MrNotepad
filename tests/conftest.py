# -*- coding: utf-8 -*-
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch

# Adiciona o diretório raiz ao path do Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def setup_path():
    """Configura o path para imports"""
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def disable_tkinter():
    """Desabilita Tkinter durante testes para evitar problemas"""
    try:
        import tkinter as tk
        original_tk = tk.Tk
        original_toplevel = tk.Toplevel
        
        def mock_tk(*args, **kwargs):
            mock = Mock()
            mock.title = Mock()
            mock.geometry = Mock()
            mock.minsize = Mock()
            mock.configure = Mock()
            mock.bind = Mock()
            mock.after = Mock()
            return mock
        
        tk.Tk = mock_tk
        tk.Toplevel = mock_tk
        
        # Patch do ttk também
        with patch('tkinter.ttk.Notebook') as mock_notebook:
            with patch('tkinter.ttk.Frame'):
                with patch('tkinter.ttk.Scrollbar'):
                    with patch('tkinter.ttk.Style'):
                        yield
    except ImportError:
        yield
    finally:
        # Restaura original se possível
        try:
            import tkinter as tk
            tk.Tk = original_tk
            tk.Toplevel = original_toplevel
        except:
            pass

@pytest.fixture
def mock_app():
    """Fixture para aplicação mockada"""
    app = Mock()
    app.root = Mock()
    app.root.title = Mock()
    app.root.geometry = Mock()
    app.root.minsize = Mock()
    app.root.configure = Mock()
    app.root.bind = Mock()
    app.root.after = Mock()
    return app

@pytest.fixture
def tab_manager(mock_app):
    """Fixture para TabManager com mocks"""
    with patch('core.tab_manager.ttk.Notebook') as mock_notebook_class:
        with patch('core.tab_manager.ttk.Frame'):
            with patch('core.tab_manager.ttk.Scrollbar'):
                with patch('core.tab_manager.tk.Text'):
                    with patch('core.tab_manager.tk.Label'):
                        
                        from core.tab_manager import TabManager
                        manager = TabManager(mock_app)
                        
                        # Configura mocks
                        mock_notebook = Mock()
                        mock_notebook_class.return_value = mock_notebook
                        manager.notebook = mock_notebook
                        
                        # Configura tabs mockadas
                        manager.tabs = {
                            "tab1": {
                                'frame': Mock(),
                                'text_area': Mock(),
                                'scrollbar': Mock(),
                                'filename': None,
                                'modified': False
                            }
                        }
                        manager.current_tab = "tab1"
                        manager.status_bar = Mock()
                        
                        yield manager

@pytest.fixture
def file_operations(mock_app):
    """Fixture para FileOperations"""
    from core.file_operations import FileOperations
    return FileOperations(mock_app)

@pytest.fixture
def event_handler(mock_app):
    """Fixture para EventHandler"""
    from core.event_handler import EventHandler
    return EventHandler(mock_app)