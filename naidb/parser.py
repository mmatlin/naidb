from ply import yacc
from .lexer import NaiDBLexer

tokens = NaiDBLexer.tokens


class Node:
    def __init__(self, type, children, value=None):
        self.type = type
        self.children = children
        self.value = value

    def __str__(self):
        # 0th level will always be program, which has value None
        out = f"[{self.type}] (0)"
        for child in self.children:
            out += f"\n--{child._str_helper(1)}"
        return out

    def _str_helper(self, level):
        out = f"[{self.type}]{' ' + str(self.value) if self.value else ''} ({level})"
        for child in self.children:
            out += f"\n{'--' * (level + 1)}{child._str_helper(level + 1) if isinstance(child, Node) else str(child)}"
        return out


def p_program(p):
    """
    program : expression program
            | expression
    """
    try:
        p[0] = Node("program", [p[1], *p[2].children])
    except IndexError:
        p[0] = Node("program", [p[1]])


def p_expression(p):
    # TODO: determine the best way to add [literal_value, expression_terminator] without conflict
    """
    expression : name expression_terminator
               | attribute expression_terminator
               | function_call expression_terminator
               | let_binding expression
    """
    p[0] = Node("expression", [p[1], p[2]])


def p_expression_terminator(p):
    """
    expression_terminator : SEMICOLON
                          | EOF
    """
    # Not the cleanest way to assign the value
    p[0] = Node("expression_terminator", list(), value=p[1] or "EOF")


def p_attribute(p):
    """
    attribute : name DOT name
              | attribute DOT name
              | name DOT function_call
              | attribute DOT function_call
    """
    p[0] = Node("attribute", [p[1], p[3]])


def p_function_call(p):
    """
    function_call : name argument_list
    """
    p[0] = Node("function_call", [p[1], p[2]])


def p_let_binding(p):
    """
    let_binding : LET name SINGLEEQUALS expression IN
                | LET function_def SINGLEEQUALS expression IN
    """
    p[0] = Node("let_binding", [p[2], p[4]])


def p_argument_list(p):
    """
    argument_list : LPAREN argument rest_of_argument_list
    """
    p[0] = Node("argument_list", [p[2], *p[3].children])


def p_rest_of_argument_list(p):
    """
    rest_of_argument_list : RPAREN
                          | COMMA argument rest_of_argument_list
    """
    if p[1] == ")":
        p[0] = Node("rest_of_argument_list", list())
    elif p[1] == ",":
        p[0] = Node("rest_of_argument_list", [p[2], *p[3].children])


def p_argument(p):
    """
    argument : named_argument
             | literal_value
    """
    p[0] = p[1]


def p_named_argument(p):
    """
    named_argument : name SINGLEEQUALS name
                   | name SINGLEEQUALS literal_value
    """
    p[0] = Node("named_argument", [p[1], p[3]])


def p_literal_value(p):
    """
    literal_value : number
                  | string
                  | attribute
                  | reference
    """
    p[0] = p[1]


def p_function_def(p):
    """
    function_def : name parameter_list
    """
    p[0] = Node("function_def", [p[1], p[2]])


def p_parameter_list(p):
    """
    parameter_list : LPAREN parameter rest_of_parameter_list
    """
    p[0] = Node("parameter_list", [p[2], *p[3].children])


def p_rest_of_parameter_list(p):
    """
    rest_of_parameter_list : RPAREN
                           | COMMA parameter rest_of_parameter_list
    """
    if p[1] == ")":
        p[0] = Node("rest_of_parameter_list", list())
    elif p[1] == ",":
        p[0] = Node("rest_of_parameter_list", [p[2], *p[3].children])


def p_parameter(p):
    """
    parameter : name COLON name
    """
    p[0] = Node("parameter", [p[1], p[3]])


def p_reference(p):
    """
    reference : DOT name
    """
    p[0] = Node("reference", [p[2]])


def p_name(p):
    """
    name : NAME
    """
    p[0] = Node("name", list(), value=p[1])


def p_number(p):
    """
    number : NUMBER
    """
    p[0] = Node("number", list(), value=p[1])


def p_string(p):
    """
    string : STRING
    """
    p[0] = Node("string", list(), value=p[1])


def p_error(p):
    print(
        f'Syntax error at line {p.lineno}, position {p.lexpos}: {p.type} "{str(p.value)}"'
    )
    # Later change this, parsing input with syntax errors shouldn't return an AST
    parser.errok()


parser = yacc.yacc()


def parse_input(input_, lexer):
    return parser.parse(input_, lexer=lexer)
