from ape import plugins
from .compiler import DasyCompiler

__version__ = '0.1.2'

@plugins.register(plugins.CompilerPlugin)
def register_compiler():
    return (".dasy",), DasyCompiler
