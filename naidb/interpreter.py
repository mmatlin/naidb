from .lexer import NaiDBLexer
from .parser import parse_input


def execute_file(input_):
    with open(input_) as input_file:
        return execute_string(input_file.read())


def execute_string(input_):
    # Currently only lexes/parses, doesn't execute
    lexer = NaiDBLexer()
    ast = parse_input(input_, lexer.lexer)
    return ast
