# Imports
import ply.lex as lex

# ------------------------------------------------- Lexico -------------------------------------------------

# Define tokens
tokens = (
    "ID",
    "CTESTRING",
    "CTEINT",
    "CTEFLOAT",
    "CTEBOOL",
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    "GREATERTHAN",
    "LESSTHAN",
    "NOTEQUAL",
    "ASSIGN",
    'LPAREN',
    'RPAREN',
    "LBRACKET",
    "RBRACKET",
    "LBRACE",
    "RBRACE",
    "COMMA",
    "COLON",
    "ENDINSTRUC"
)

# Define token regular expressions
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GREATERTHAN = r'\>'
t_LESSTHAN = r'\<'
t_NOTEQUAL = r'\!='
t_ASSIGN = r'\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'
t_COLON = r'\:'
t_ENDINSTRUC = r'\;'

# Define reserved keywords
reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    "program": "PROGRAM",
    "main": "MAIN",
    "end": "END",
    "var": "VAR",
    "print": "PRINT",
    "void": "VOID",
    "while": "WHILE",
    "do": "DO",
    "int": "INT",
    "float": "FLOAT",
    "bool": "BOOL",
    "and": "AND",
    "or": "OR"
}

# Combine the tokens and reserved keywords
tokens = tokens + tuple(reserved.values())

# Define a rule for floating numbers
def t_CTEFLOAT(t):
    r'[-+]?[0-9]*\.[0-9]+'
    t.value = float(t.value)
    return t

# Define a rule for integer numbers
def t_CTEINT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Define a rule for strings
def t_CTESTRING(t):
    r'"([^"]*)"'
    t.value = str(t.value)
    return t

# Define a rule for boolean values
def t_CTEBOOL(t):
    r'true|false'
    t.value = t.value == 'true'
    return t

# Define a rule for IDs
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t

# Define how to handle whitespace
t_ignore = ' \t'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Define error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()