# Imports
import lex
import yacc
from collections import deque

# ------------------------------------------------- Tabla de consideraciones semanticas (cubo semantico) -------------------------------------------------

# Definir los tipos y operadores
tipos = ['int', 'float', 'bool']
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

cubo_semantico['float']['float']['+'] = 'float'
cubo_semantico['float']['float']['-'] = 'float'
cubo_semantico['float']['float']['*'] = 'float'
cubo_semantico['float']['float']['/'] = 'float'

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
cubo_semantico['int']['int']['!='] = 'bool'
cubo_semantico['int']['int']['<'] = 'bool'
cubo_semantico['int']['int']['>'] = 'bool'

cubo_semantico['float']['float']['!='] = 'bool'
cubo_semantico['float']['float']['<'] = 'bool'
cubo_semantico['float']['float']['>'] = 'bool'

cubo_semantico['int']['float']['!='] = 'bool'
cubo_semantico['float']['int']['!='] = 'bool'
cubo_semantico['int']['float']['<'] = 'bool'
cubo_semantico['float']['int']['<'] = 'bool'
cubo_semantico['int']['float']['>'] = 'bool'
cubo_semantico['float']['int']['>'] = 'bool'

# ------------------------------------------------- Directorio de funciones y variables -------------------------------------------------

funcs_dir = {
    'global': {
        'vars': {}
    }
}

current_scope = 'global'

# ------------------------------------------------- Helper functions -------------------------------------------------

# Function that returns the expected type of an operation
def get_expected_type(left_operand, right_operand, operator):
    if cubo_semantico[left_operand][right_operand][operator]:
        return cubo_semantico[left_operand][right_operand][operator]
    else:
        raise TypeError(f"'{operator}' is not supported between instances of '{left_operand}' and '{right_operand}'")

# Function that checks the type of a given operand
def get_operand_type(operand):
    # Get the current scope variable

    print("------------------ Received Operand: ", operand)

    # Initialize the return var
    operand_type = ""

    # First check if we are not in global in order to also look into those variables
    if current_scope != "global":
        # Check the types of the operands
        if operand in funcs_dir[current_scope]["vars"]:
            operand_type = funcs_dir[current_scope]["vars"][operand]
        elif operand in funcs_dir["global"]["vars"]:
            operand_type = funcs_dir["global"]["vars"][operand]
        else:
            if isinstance(operand, bool):
                operand_type = "bool"
            elif isinstance(operand, int):
                operand_type = "int"
            elif isinstance(operand, float):
                operand_type = "float"
            else:
                raise ReferenceError(f"'{operand}' is not defined")
    else:
        if operand in funcs_dir[current_scope]["vars"]:
            operand_type = funcs_dir[current_scope]["vars"][operand]
        else:
            if isinstance(operand, bool):
                operand_type = "bool"
            elif isinstance(operand, int):
                operand_type = "int"
            elif isinstance(operand, float):
                operand_type = "float"
            else:
                raise ReferenceError(f"'{operand}' is not defined")

    return operand_type


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
    "bool": "BOOL"
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

# ------------------------------------------------- Define grammar rules (Syntax Parser) -------------------------------------------------

def p_prog(p):
    "prog : PROGRAM ID ENDINSTRUC vars funcs mas_funcs MAIN body END"
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

    # Loop the list of vars
    print("------------------- type stack: ", current_type_stack)
    print("------------------- var name stack: ", current_var_stack)
    print("------------------- p1: ", p[1])
    for var_name in p[1]:
        current_var_stack.append(var_name)

    # Get the type of the n coming variables
    vars_type = current_type_stack.pop()

    # Pop the vars and types and add them to the directories
    while current_var_stack:
        var_name = current_var_stack.pop()

        # Check scope
        if current_scope in funcs_dir:
            if var_name in funcs_dir[current_scope]['vars']:
                raise ReferenceError(f"'{var_name}' variable has already been declared")
            else:
                funcs_dir[current_scope]['vars'][var_name] = vars_type
        else:
            funcs_dir[current_scope] = {'vars': {var_name: vars_type}}

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
            | FLOAT
            | BOOL"""
    p[0] = p[1]
    current_type_stack.append(p[1])

def p_funcs(p):
    """funcs : func_start LPAREN list_params RPAREN LBRACKET vars body RBRACKET ENDINSTRUC
            | empty"""

    # Check if we have a function
    if len(p) == 10:
        # Get current scope global variable
        global current_scope

        # Reset current scope to global
        current_scope = "global"

        print("------------------- Current scope after finish func: ", current_scope)
        print("------------------- func dir: ", funcs_dir)

        p[0] = ('func', p[1], p[3], p[6], p[7])
    else:
        p[0] = None

def p_func_start(p):
    """func_start : VOID ID"""

    # Set the global variable current scope to be the new function
    global current_scope
    current_scope = p[2]

    print("------------------- Current scope: ", current_scope)

    # Check if we already have the function declared in out func dir
    if current_scope in funcs_dir:
        raise ReferenceError(f"'{current_scope}' function has already been declared")

    p[0] = p[2]

def p_mas_funcs(p):
    """mas_funcs : funcs
            | empty"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = None

def p_list_params(p):
    """list_params : ID COLON type mas_params
                    | empty"""

    # Get current scope global variable
    global current_scope

    if len(p) == 5:
        # Get name and type of param
        param_name = p[1]
        param_type = p[3]

        # Check scope
        if current_scope in funcs_dir:
            # Check if we have one already declared within the scope
            if param_name in funcs_dir[current_scope]['vars']:
                raise ReferenceError(f"'{param_name}' variable has already been declared in this function '{current_scope}'")
            else:
                funcs_dir[current_scope]['vars'][param_name] = param_type
        else:
            funcs_dir[current_scope] = {'vars': {param_name: param_type}}

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
    print("-------------------- We are at body")

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
    # Get the var and value
    variable_name = p[1]
    assigned_value = p[3]
    assigned_type = operand_stack.pop()

    print("-------------------- Assigned val", assigned_value)
    print("-------------------- Assigned val", assigned_type)

    if variable_name not in funcs_dir[current_scope]["vars"]:
        raise ReferenceError(f"Assignment to undeclared variable '{variable_name}'")
    elif funcs_dir[current_scope]["vars"][variable_name] != assigned_type:
        expected_type = funcs_dir[current_scope]["vars"][variable_name]
        raise TypeError(f"Result type must be '{expected_type}', not '{assigned_type}'")
    else:
        p[0] = ['assign', variable_name, assigned_value]

def p_expresion(p):
    "expresion : exp mas_expresiones"
    print("-------------------- Expresion rule")
    if p[2] is None:
        p[0] = p[1]
    else:
        operator, right_exp = p[2]
        print("-------------------- Operator", operator)
        print("-------------------- left", p[1])
        print("-------------------- right", right_exp)

        # Pop the last types
        right_operand_type = operand_stack.pop()
        left_operand_type = operand_stack.pop()

        # Check expected type
        result_type = get_expected_type(left_operand_type, right_operand_type, operator)

        # Push the new result type to the stack
        operand_stack.append(result_type)
        print("-------------------- Result type: ", result_type)
        print("-------------------- Operand stack: ", operand_stack)

        p[0] = [operator, p[1], right_exp]

def p_mas_expresiones(p):
    """mas_expresiones : GREATERTHAN exp
                        | LESSTHAN exp
                        | NOTEQUAL exp
                        | empty"""
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = None

def p_exp(p):
    "exp : termino mas_exp"
    print("-------------------- Exp rule")
    if len(p) == 3:
        print("-------------------- p1: ", p[1])
        print("-------------------- p2: ", p[2])
        if p[2] is None:
            p[0] = p[1]
        else:
            operator = p[2][0]

            # Pop the last types
            right_operand_type = operand_stack.pop()
            left_operand_type = operand_stack.pop()

            # Check expected type
            result_type = get_expected_type(left_operand_type, right_operand_type, operator)

            # Push the new result type to the stack
            operand_stack.append(result_type)
            print("-------------------- Result type: ", result_type)
            print("-------------------- Operand stack: ", operand_stack)

            p[0] = [p[1]] + p[2]
    else:
        p[0] = None

def p_mas_exp(p):
    """mas_exp : PLUS exp
                | MINUS exp
                | empty"""
    print("-------------------- mas Exp rule")
    print("-------------------- p1: ", p[1])
    if p[1] != None:
        p[0] = [p[1], p[2]]

def p_termino(p):
    "termino : factor mas_terminos"
    print("-------------------- termino rule")
    if p[2] is None:
        p[0] = p[1]
    else:
        left_termino = p[1]
        operator, right_termino = p[2]
        print("-------------------- Operator", operator)
        print("-------------------- left", p[1])
        print("-------------------- right", right_termino)

        # Pop the last types
        right_operand_type = operand_stack.pop()
        left_operand_type = operand_stack.pop()

        # Check expected type
        result_type = get_expected_type(left_operand_type, right_operand_type, operator)

        # Push the new result type to the stack
        operand_stack.append(result_type)
        print("-------------------- Result type: ", result_type)
        print("-------------------- Operand stack: ", operand_stack)

        p[0] = [operator, left_termino, right_termino]


def p_mas_terminos(p):
    """mas_terminos : TIMES termino
                    | DIVIDE termino
                    | empty"""
    print("-------------------- mas terminos rule")
    if len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = None

def p_factor(p):
    """factor : LPAREN expresion RPAREN
                | factor_opt
                | PLUS factor_opt
                | MINUS factor_opt"""
    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = [p[1], p[2]]
    else:
        p[0] = p[1]

def p_factor_opt(p):
    """factor_opt : cte
                    | ID"""
    print("--------------------- factor opt: ")
    operand_type = get_operand_type(p[1])
    print("--------------------- operand type: ", operand_type)
    operand_stack.append(operand_type)
    print("--------------------- operand stack: ", operand_stack)
    p[0] = p[1]

def p_cte(p):
    """cte : CTEINT
            | CTEFLOAT
            | CTEBOOL"""
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
program test3;

var x: int;

void hello (i: int, x: float) [
    var y: float;
    {
        x = y * i;
    }
];

void bye (m: bool) [
    var y: float;
    {
        m = x > y;
    }
];

main
{
    x = 1 + 2;
}
end
"""

# Initialize stacks
current_type_stack = deque()
current_var_stack = deque()
operand_stack = deque()

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
lexer.input(test)

# Build parser
parser = yacc.yacc(start="prog", debug=True)

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
print("Function and Vars Directory: ")
for key in funcs_dir:
    print(key + ": ")
    print(funcs_dir[key])
    print()