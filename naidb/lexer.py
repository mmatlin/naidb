from ply import lex


class NaiDBLexer:
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input_(self, data):
        self.lexer.input(data)

    def get_token(self):
        while token := self.lexer.token():
            yield token

    def get_tokens(self):
        return (token for token in self.get_token())

    reserved = {
        "let": "LET",
        "in": "IN",
        "if": "IF",
        "then": "THEN",
        "else": "ELSE",
        "and": "AND",
        "or": "OR",
    }

    tokens = [
        "NAME",
        "NEWLINE",
        "NUMBER",
        "LPAREN",
        "RPAREN",
        "LBRACKET",
        "RBRACKET",
        "LBRACE",
        "RBRACE",
        "SINGLEQUOTE",
        "DOUBLEQUOTE",
        "COLON",
        "HASH",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVISION",
        "DOUBLEEQUALS",
        "SINGLEEQUALS",
        "DOT",
        "COMMA",
    ] + list(reserved.values())

    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"
    t_LBRACE = r"\{"
    t_RBRACE = r"\}"
    t_SINGLEQUOTE = r"'"
    t_DOUBLEQUOTE = r'"'
    t_COLON = r":"
    t_HASH = r"[#]"
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVISION = r"/"
    t_DOUBLEEQUALS = r"=="
    t_SINGLEEQUALS = r"="
    t_DOT = r"\."
    t_COMMA = r","

    t_ignore_COMMENT = r"//.*"
    t_ignore = " \t"

    def t_NAME(self, t):
        r"\w+"
        t.type = NaiDBLexer.reserved.get(t.value, "NAME")
        return t

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        return t

    # TODO: define t_error rule
