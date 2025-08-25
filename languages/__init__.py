from .python import PythonSupport
from .rust import RustSupport

class LanguageManager:
    def __init__(self, app):
        self.app = app
        self.supported_languages = {
            '.rs': RustSupport(app),
            '.py': PythonSupport(app),
            '.txt': None,
        }

    def get_languages_support(self, filename):
        #retorna o suporte a linguagem
        pass

    def has_language_support(self, filename):
        #Verifica se há suporte
        return self.get_languages_support(filename) is not None