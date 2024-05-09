# Imports
import lex
import yacc

# Define tokens
tokens = (
    "ID",
    "CTESTRING",
    "CTEINT",
    "CTEFLOAT",
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
    "float": "FLOAT"
}

# Combine the tokens and reserved keywords
tokens = tokens + tuple(reserved.values())

# Define a rule for IDs
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') # Check for reserved words
    return t

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
    r'"[a-zA-Z_][a-zA-Z_0-9]*"'
    t.value = str(t.value)
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

# ------------------------------------------------- Define grammar rules (Syntax Parser) -------------------------------------------------

# Define parser precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_prog(p):
    "prog : PROGRAM ID ENDINSTRUC vars funcs MAIN body END"

def p_vars(p):
    """vars : VAR variables
            | empty"""

def p_variables(p):
    "variables : list_ids COLON type ENDINSTRUC mas_vars"

def p_list_ids(p):
    "list_ids : ID mas_ids"

def p_mas_ids(p):
    """mas_ids : COMMA list_ids
                | empty"""

def p_mas_vars(p):
    """mas_vars : variables
                | empty"""

def p_type(p):
    """type : INT
            | FLOAT"""

def p_funcs(p):
    """funcs : VOID ID LPAREN list_params RPAREN LBRACKET vars body RBRACKET
            | empty"""

def p_list_params(p):
    """list_params : ID COLON type mas_params
                    | empty"""

def p_mas_params(p):
    """mas_params : COMMA list_params
                    | empty"""

def p_body(p):
    "body : LBRACE list_statements RBRACE"

def p_statement(p):
    """statement : assign
                | condition
                | cycle
                | f_call
                | print"""

def p_list_statements(p):
    """list_statements : statement more_statements
                        | empty"""

def p_more_statements(p):
    "more_statements : list_statements"

def p_assign(p):
    "assign : ID ASSIGN expresion ENDINSTRUC"

def p_expresion(p):
    "expresion : exp mas_expresiones"

def p_mas_expresiones(p):
    """mas_expresiones : GREATERTHAN exp
                        | LESSTHAN exp
                        | NOTEQUAL exp
                        | empty"""

def p_exp(p):
    "exp : termino mas_exp"

def p_mas_exp(p):
    """mas_exp : PLUS exp
                | MINUS exp
                | empty"""

def p_termino(p):
    "termino : factor mas_terminos"

def p_mas_terminos(p):
    """mas_terminos : TIMES termino
                    | DIVIDE termino
                    | empty"""

def p_factor(p):
    """factor : LPAREN expresion RPAREN
                | factor_opt
                | PLUS factor_opt
                | MINUS factor_opt"""

def p_factor_opt(p):
    """factor_opt : cte
                    | ID"""

def p_cte(p):
    """cte : CTEINT
            | CTEFLOAT"""

def p_condition(p):
    "condition : IF LPAREN expresion RPAREN body else_block ENDINSTRUC"

def p_else_block(p):
    """else_block : ELSE body
            | empty"""

def p_cycle(p):
    "cycle : WHILE body DO LPAREN expresion RPAREN ENDINSTRUC"

def p_f_call(p):
    "f_call : ID LPAREN list_exp RPAREN ENDINSTRUC"

def p_list_exp(p):
    """list_exp : expresion mas_list_exp
                | empty"""

def p_mas_list_exp(p):
    """mas_list_exp : COMMA list_exp
                    | empty"""

def p_print(p):
    "print : PRINT LPAREN print_opt RPAREN ENDINSTRUC"

def p_print_opt(p):
    """print_opt : list_exp more_opt
                | CTESTRING more_opt"""

def p_more_opt(p):
    """more_opt : COMMA print_opt
                | empty"""

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Error de sintaxis en la entrada:", p)

# Build pareser
parser = yacc.yacc(start="prog", debug=True)

# Test
basic_program_data = """
program test;

var i, j: int;

void max(i: int, j: int) [
    {
        if (i > j) {
            print(i);
        } else {
            print(j);
        };
    }
]

main
{
    i = 5;
    j = 10;
    max(i, j);

    while { check = i < 10; } do ( i + 1 );
}
end
"""

# Give the lexer some input
lexer.input(basic_program_data)

# Tokenize
print("")
print("-------------------------- Scanner --------------------------")
print("")
while True:
    tok = lexer.token()
    if not tok:
        break # No more input
    print(tok)
print("")
print("-------------------------------------------------------------")
print("")

# Parse the input and get the results
result = parser.parse(basic_program_data)
print("")
print("-------------------------- Parser --------------------------")
print("")
print(basic_program_data)
print("")
print("------------------------------------------------------------")
print("")