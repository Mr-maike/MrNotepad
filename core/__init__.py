# -*- coding: utf-8 -*-
"""
MrNotepad Core Package
======================

Módulos principais do editor de texto MrNotepad.
"""

# Importações principais para facilitar o acesso
from .app import MrNotepad
from .file_operations import FileOperations
from .text_editor import TextEditor
from .menu_manager import MenuManager
from .event_handler import EventHandler

# Versão do pacote core
__version__ = '1.0.0'
__author__ = 'Mr-maike'
__email__ = 'seu-email@exemplo.com'

# Lista de módulos exportados
__all__ = [
    'MrNotepad',
    'FileOperations', 
    'TextEditor',
    'MenuManager',
    'EventHandler'
]

# Inicialização do pacote
print(f"MrNotepad Core {__version__} carregado")