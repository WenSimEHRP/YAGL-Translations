import pprint

import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    "STRING",
    "NUMBER",
    "COLON",
    "SEMICOLON",
    "LBRACE",
    "RBRACE",
    "LSQUARE",
    "RSQUARE",
    "SMALLER",
    "GREATER",
    "ID",
    "COMMA",
    "COMMENT",
)

# Regular expression rules for simple tokens
t_COLON = r":"
t_SEMICOLON = r";"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LSQUARE = r"\["
t_RSQUARE = r"\]"
t_SMALLER = r"<"
t_GREATER = r">"
t_COMMA = r","

# A regular expression rule with some action code
def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    return t


def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\" "
    t.value = t.value[1:-1]  # Remove the quotes
    return t


def t_NUMBER(t):
    # also match hex numbers
    r"0x[0-9a-fA-F]+|\d+" # Match hex and decimal numbers
    if t.value.startswith("0x"):
        t.value = int(t.value, 16)
    else:
        t.value = int(t.value)
    return t

def t_COMMENT(t):
    r"//.*"
    pass  # Ignore comments

# Define a rule so we can track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = " \t"


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer

def p_start_body(p):
    """start_body : start_body start
    | start"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_start(p):
    """start : tree
    | assignment
    | properties"""
    p[0] = p[1]

def p_properties(p):
    """properties : ID decorator LBRACE properties_body RBRACE"""
    p[0] = (p[1], p[2], p[4])

def p_properties_body(p):
    """properties_body : properties_body properties_assignment
    | properties_assignment"""
    if len(p) == 3:
        p[0] = p[1] + (p[2],)
    else:
        p[0] = (p[1],)

def p_properties_assignment(p):
    """properties_assignment : LBRACE assignment RBRACE"""
    p[0] = p[2]

def p_error(p):
    if p:
        # print out some more useful information
        print(f"Syntax error at '{p.value}' (line {p.lineno}, pos {p.lexpos})")
    else:
        print("Syntax error at EOF")

def p_list(p):
    """list : LSQUARE value RSQUARE"""
    p[0] = ("list", p[2])

def p_decorator(p):
    """decorator : SMALLER value GREATER"""
    p[0] = ("decorator", p[2])

def p_value(p):
    """value : value COMMA value
    | value value
    | STRING
    | NUMBER
    | ID
    | list"""
    if len(p) == 4:
        if isinstance(p[3], tuple):
            p[0] = (p[1], *p[3])
        else:
            p[0] = (p[1], p[3])
    elif len(p) == 3:
        if isinstance(p[2], tuple):
            p[0] = (p[1], *p[2])
        else:
            p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_id_number(p):
    """id_number : ID
    | NUMBER"""
    p[0] = p[1]

def p_assignment_body(p):
    """assignment_body : assignment_body assignment
    | assignment"""
    if len(p) == 3:
        p[0] = p[1] + (p[2],)
    else:
        p[0] = (p[1],)

def p_assignment(p):
    """assignment : id_number COLON value SEMICOLON
    | id_number COLON LBRACE assignment_body RBRACE"""
    if len(p) == 5:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[1], p[4])

def p_tree(p):
    """tree : ID LBRACE assignment_body RBRACE"""
    p[0] = (p[1], p[3])



lexer = lex.lex()
parser = yacc.yacc()

with open("data.txt", "r") as f:
    data = f.read()

lexer.input(data)
for tok in lexer:
    print(tok)

result = parser.parse(data)
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(result)
