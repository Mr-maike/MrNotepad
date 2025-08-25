from .compiler import RustCompiler
from .syntax import RustSyntaxHighlighter

class RustSupport:
    def __init__(self, app):
        self.app = app
        self.compiler = RustCompiler(app)
        self.syntax = RustSyntaxHighlighter(app)

    def setup(self):
        #configura o suporte para o Rust
        self.syntax.setup_highlighting()

    def compile_and_run(self):
        return self.compiler.comile_and_run()