import tkinter as tk
from .text_editor import TextEditor
from .file_operations import FileOperations
from .event_handler import EventHandler
from .menu_manager import MenuManager

class MrNotepad:
    def __init__(self, root):
        self.root = root
        self.setup_window()

        self.text_editor = TextEditor(self)
        self.file_operations = FileOperations(self)
        self.menu_manager = MenuManager(self)
        self.event_handler = EventHandler(self)

    def setup_window(self):
        self.root.title('Untitled - MrNotepad')
        self.root.geometry('800x600')
        self.root.minsize(600, 500)
