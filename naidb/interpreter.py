from .lexer import NaiDBLexer


def execute_file(input_):
    with open(input_) as input_file:
        return execute_string(input_file.read())


def execute_string(input_):
    lexer = NaiDBLexer()
    lexer.input_(input_)
    tokens = lexer.get_tokens()
    return tuple(tokens)
