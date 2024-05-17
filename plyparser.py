# Imports
from collections import deque
import ply.yacc as yacc
from plylexer import tokens
from helper_funcs import get_expected_type, get_operand_type
from globals import current_scope, funcs_dir

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

    # Get every var name from list ids
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

        p[0] = ('func', p[1], p[3], p[6], p[7])
    else:
        p[0] = None

def p_func_start(p):
    """func_start : VOID ID"""

    # Set the global variable current scope to be the new function
    global current_scope
    current_scope = p[2]

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
    # Get the var name assigned value expresion and type of that value
    variable_name = p[1]
    assigned_value = p[3]
    assigned_type = operand_stack.pop()

    # Check first if the variable name was actually declared if so check if the types are correct
    if variable_name not in funcs_dir[current_scope]["vars"]:
        raise ReferenceError(f"Assignment to undeclared variable '{variable_name}'")
    elif funcs_dir[current_scope]["vars"][variable_name] != assigned_type:
        expected_type = funcs_dir[current_scope]["vars"][variable_name]
        raise TypeError(f"Result type must be '{expected_type}', not '{assigned_type}'")
    else:
        p[0] = ['assign', variable_name, assigned_value]

def p_expresion(p):
    "expresion : exp mas_expresiones"
    if p[2] is None:
        p[0] = p[1]
    else:
        # Get operator and right operand
        operator, right_exp = p[2]

        # Pop the last types
        right_operand_type = operand_stack.pop()
        left_operand_type = operand_stack.pop()

        # Check expected type
        result_type = get_expected_type(left_operand_type, right_operand_type, operator)

        # Push the new result type to the stack
        operand_stack.append(result_type)

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
    if len(p) == 3:
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

            p[0] = [p[1]] + p[2]
    else:
        p[0] = None

def p_mas_exp(p):
    """mas_exp : PLUS exp
                | MINUS exp
                | empty"""
    if p[1] != None:
        p[0] = [p[1], p[2]]

def p_termino(p):
    "termino : factor mas_terminos"
    if p[2] is None:
        p[0] = p[1]
    else:
        left_termino = p[1]
        operator, right_termino = p[2]

        # Pop the last types
        right_operand_type = operand_stack.pop()
        left_operand_type = operand_stack.pop()

        # Check expected type
        result_type = get_expected_type(left_operand_type, right_operand_type, operator)

        # Push the new result type to the stack
        operand_stack.append(result_type)

        p[0] = [operator, left_termino, right_termino]


def p_mas_terminos(p):
    """mas_terminos : TIMES termino
                    | DIVIDE termino
                    | empty"""
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

    # Get operand type if it exist in our vars table
    operand_type = get_operand_type(p[1])

    # Add it to the operand stack to keep track
    operand_stack.append(operand_type)

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
    p[0] = (p[1], p[2])

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

# ------------------------------------------------- Initialize stacks -------------------------------------------------

current_type_stack = deque()
current_var_stack = deque()
operand_stack = deque()

# Build parser
parser = yacc.yacc(start="prog")