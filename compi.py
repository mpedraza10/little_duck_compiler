# Imports
import lex
import yacc

# ------------------------------------------------- Tabla de consideraciones semanticas (cubo semantico) -------------------------------------------------

# Definir los tipos y operadores
tipos = ['int', 'float']
operadores = ['+', '-', '*', '/', '!=', '<', '>']

# Crear un cubo semántico vacío
cubo_semantico = {}

# Inicializar el cubo semántico
for tipo1 in tipos:
    cubo_semantico[tipo1] = {}
    for tipo2 in tipos:
        cubo_semantico[tipo1][tipo2] = {}
        for operador in operadores:
            cubo_semantico[tipo1][tipo2][operador] = None

# Ejemplo de llenado del cubo semántico para algunos operadores
cubo_semantico['int']['int']['+'] = 'int'
cubo_semantico['int']['int']['-'] = 'int'
cubo_semantico['int']['int']['*'] = 'int'
cubo_semantico['int']['int']['/'] = 'float'
cubo_semantico['int']['float']['+'] = 'float'
cubo_semantico['float']['int']['+'] = 'float'
cubo_semantico['int']['float']['-'] = 'float'
cubo_semantico['float']['int']['-'] = 'float'
cubo_semantico['int']['float']['-'] = 'float'
cubo_semantico['float']['int']['-'] = 'float'
cubo_semantico['int']['float']['*'] = 'float'
cubo_semantico['float']['int']['*'] = 'float'
cubo_semantico['int']['float']['/'] = 'float'
cubo_semantico['float']['int']['/'] = 'float'

# Ejemplo para operadores relacionales
cubo_semantico['int']['int']['!='] = 'int'
cubo_semantico['int']['int']['<'] = 'int'
cubo_semantico['int']['int']['>'] = 'int'

def obtener_tipo_resultado(operando1, operando2, operador):
    tipo1 = type(operando1).__name__
    tipo2 = type(operando2).__name__

    # Verificar si los tipos y el operador están en el cubo semántico
    if tipo1 in cubo_semantico and tipo2 in cubo_semantico[tipo1] and operador in cubo_semantico[tipo1][tipo2]:
        resultado = cubo_semantico[tipo1][tipo2][operador]
        if resultado:
            return resultado
        else:
            raise TypeError(f"Operación inválida: {tipo1} {operador} {tipo2}")
    else:
        raise TypeError(f"Operación inválida o no soportada: {tipo1} {operador} {tipo2}")

# Ejemplo de uso
"""
try:
    tipo_res = obtener_tipo_resultado(1, "a", '+')
    print(f"Resultado tipo: {tipo_res}")
except TypeError as e:
    print(e)
"""

# ------------------------------------------------- Directorio de funciones y variables -------------------------------------------------

directorio_funciones = {
    'global': {
        'type': 'void',
        'parametros': [],
        'variables': "global_vars"
    }
}

# ------------------------------------------------- Lexico -------------------------------------------------

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
    r'"([^"]*)"'
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
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'PLUS', 'MINUS'),
    ('right', 'UPLUS'), # Unary plus
    ('right', 'UMINUS'), # Unary minus
)

def p_prog(p):
    "prog : PROGRAM ID ENDINSTRUC vars funcs MAIN body END"
    p[0] = ('prog', p[2], p[4], p[5], p[7])

def p_vars(p):
    """vars : VAR variables
            | empty"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_variables(p):
    "variables : list_ids COLON type ENDINSTRUC mas_vars"
    p[0] = ('vars', p[1], p[3], p[5])

def p_list_ids(p):
    "list_ids : ID mas_ids"
    p[0] = [p[1]] + p[2]

def p_mas_ids(p):
    """mas_ids : COMMA list_ids
                | empty"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_mas_vars(p):
    """mas_vars : variables
                | empty"""
    if p[1] is not None:
        p[0] = p[1]
    else:
        p[0] = []

def p_type(p):
    """type : INT
            | FLOAT"""
    p[0] = p[1]

def p_funcs(p):
    """funcs : VOID ID LPAREN list_params RPAREN LBRACKET vars body RBRACKET ENDINSTRUC
            | empty"""
    if len(p) == 11:
        p[0] = ('func', p[2], p[4], p[7], p[8])
    else:
        p[0] = None

def p_list_params(p):
    """list_params : ID COLON type mas_params
                    | empty"""
    if len(p) == 5:
        p[0] = [(p[1], p[3])] + p[4]
    else:
        p[0] = []

def p_mas_params(p):
    """mas_params : COMMA list_params
                    | empty"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_body(p):
    "body : LBRACE list_statements RBRACE"
    p[0] = p[2]

def p_statement(p):
    """statement : assign
                | condition
                | cycle
                | f_call
                | print"""
    p[0] = p[1]

def p_list_statements(p):
    """list_statements : statement more_statements
                        | empty"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_more_statements(p):
    "more_statements : list_statements"
    p[0] = p[1]

def p_assign(p):
    "assign : ID ASSIGN expresion ENDINSTRUC"
    p[0] = ('assign', p[1], p[3])

def p_expresion(p):
    "expresion : exp mas_expresiones"
    if p[2] is None:
        p[0] = p[1]
    else:
        operator, right_exp = p[2]
        p[0] = (operator, p[1], right_exp)

def p_mas_expresiones(p):
    """mas_expresiones : GREATERTHAN exp
                        | LESSTHAN exp
                        | NOTEQUAL exp
                        | empty"""
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None

def p_exp(p):
    "exp : termino mas_exp"
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None

def p_mas_exp(p):
    """mas_exp : PLUS exp
                | MINUS exp
                | empty"""
    if p[1] != None:
        p[0] = (p[1], p[2])

def p_termino(p):
    "termino : factor mas_terminos"
    if p[2] is None:
        p[0] = p[1]
    else:
        operator, right_termino = p[2]
        p[0] = (operator, p[1], right_termino)


def p_mas_terminos(p):
    """mas_terminos : TIMES termino
                    | DIVIDE termino
                    | empty"""
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = None

def p_factor(p):
    """factor : LPAREN expresion RPAREN
                | factor_opt
                | PLUS factor_opt %prec UPLUS
                | MINUS factor_opt %prec UMINUS"""
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_factor_opt(p):
    """factor_opt : cte
                    | ID"""
    p[0] = p[1]

def p_cte(p):
    """cte : CTEINT
            | CTEFLOAT"""
    p[0] = p[1]

def p_condition(p):
    "condition : IF LPAREN expresion RPAREN body else_block ENDINSTRUC"
    p[0] = ('if', p[3], p[5], p[6])

def p_else_block(p):
    """else_block : ELSE body
            | empty"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_cycle(p):
    "cycle : DO body WHILE LPAREN expresion RPAREN ENDINSTRUC"
    p[0] = ('do_while', p[2], p[5])

def p_f_call(p):
    "f_call : ID LPAREN list_exp RPAREN ENDINSTRUC"
    p[0] = ('f_call', p[1], p[3])

def p_list_exp(p):
    """list_exp : expresion mas_list_exp
                | empty"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_mas_list_exp(p):
    """mas_list_exp : COMMA list_exp
                    | empty"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_print(p):
    "print : PRINT LPAREN print_opt RPAREN ENDINSTRUC"
    p[0] = ('print', p[3])

def p_print_opt(p):
    """print_opt : expresion more_opt
                | CTESTRING more_opt"""
    if isinstance(p[1], str):
        p[0] = ('string', p[1], p[2])
    else:
        p[0] = ('exp', p[1], p[2])

def p_more_opt(p):
    """more_opt : COMMA print_opt
                | empty"""
    if len(p) == 3:
        p[0] = [p[2]]
    else:
        p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Error de sintaxis en la entrada:", p)

# Build pareser
parser = yacc.yacc(start="prog", debug=True)

# ------------------------------------------------- Test -------------------------------------------------
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
];

main
{
    i = 5;
    j = 10;
    print("The max value between i=", i, " and j is=", j, " is: ");
    max(i, j);

    do { i = i + 1; } while ( i < j );
}
end
"""
test = """
program test2;

var i: int;

main
{
    i = 5 * 2;
}
end
"""

# Give the lexer some input
lexer.input(test)

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
parse_tree = parser.parse(test, debug=True)
print("")
print("-------------------------- Parser --------------------------")
print("")
print("Parse Tree: ", parse_tree)
print("")
print("------------------------------------------------------------")
print("")