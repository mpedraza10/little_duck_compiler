# Imports
from collections import deque
import ply.yacc as yacc
from plylexer import tokens
from helper_funcs import get_expected_type, get_operand_type
import globals

# ------------------------------------------------- Define grammar rules (Syntax Parser) -------------------------------------------------

# Define the precedence and associativity of operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'GREATERTHAN', 'LESSTHAN', 'NOTEQUAL'),
    ('right', 'UMINUS', 'UPLUS'),  # Unary minus and plus
)

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

    # Pop the vars and types and add them to the directories
    while current_var_stack:
        var_name = current_var_stack.pop()

        # Check scope
        if globals.current_scope in globals.funcs_dir:
            if var_name in globals.funcs_dir[globals.current_scope]['vars']:
                raise ReferenceError(f"'{var_name}' variable has already been declared")
            else:
                globals.funcs_dir[globals.current_scope]['vars'][var_name] = vars_type
        else:
            globals.funcs_dir[globals.current_scope] = {'vars': {var_name: vars_type}}

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
        # Reset current scope to global
        globals.current_scope = "global"

        p[0] = ('func', p[1], p[3], p[6], p[7])
    else:
        p[0] = None

def p_func_start(p):
    """func_start : VOID ID"""

    # Set the global variable current scope to be the new function
    globals.current_scope = p[2]

    # Check if we already have the function declared in out func dir
    if globals.current_scope in globals.funcs_dir:
        raise ReferenceError(f"'{globals.current_scope}' function has already been declared")

    p[0] = p[2]

def p_mas_funcs(p):
    "mas_funcs : funcs"
    p[0] = p[1]

def p_list_params(p):
    """list_params : ID COLON type mas_params
                    | empty"""

    if len(p) == 5:
        # Get name and type of param
        param_name = p[1]
        param_type = p[3]

        # Check scope
        if globals.current_scope in globals.funcs_dir:
            # Check if we have one already declared within the scope
            if param_name in globals.funcs_dir[globals.current_scope]['vars']:
                raise ReferenceError(f"'{param_name}' variable has already been declared in this function '{globals.current_scope}'")
            else:
                globals.funcs_dir[globals.current_scope]['vars'][param_name] = param_type
        else:
            globals.funcs_dir[globals.current_scope] = {'vars': {param_name: param_type}}

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
    assigned_type = operand_type_stack.pop()

    # Check first if the variable name was actually declared if so check if the types are correct
    if variable_name not in globals.funcs_dir[globals.current_scope]["vars"]:
        raise ReferenceError(f"Assignment to undeclared variable '{variable_name}'")
    elif globals.funcs_dir[globals.current_scope]["vars"][variable_name] != assigned_type:
        expected_type = globals.funcs_dir[globals.current_scope]["vars"][variable_name]
        raise TypeError(f"Result type must be '{expected_type}', not '{assigned_type}'")
    else:
        globals.quadruples_queue.add_quadruple('=', assigned_value, None, variable_name)
        p[0] = ['assign', variable_name, assigned_value]

def p_expresion(p):
    """expresion : exp
                | exp GREATERTHAN exp
                | exp LESSTHAN exp
                | exp NOTEQUAL exp"""

    if len(p) == 2:
        p[0] = p[1]
    else:
        # Pop the last types
        right_operand_type = operand_type_stack.pop()
        left_operand_type = operand_type_stack.pop()

        # Check expected type
        result_type = get_expected_type(left_operand_type, right_operand_type, p[2])

        # Push the new result type to the stack
        operand_type_stack.append(result_type)

        temp_var = globals.quadruples_queue.new_temp()
        globals.quadruples_queue.add_quadruple(p[2], p[1], p[3], temp_var)
        p[0] = temp_var

def p_exp(p):
    """exp : exp PLUS exp
            | exp MINUS exp"""

    # Pop the last types
    right_operand_type = operand_type_stack.pop()
    left_operand_type = operand_type_stack.pop()

    # Check expected type
    result_type = get_expected_type(left_operand_type, right_operand_type, p[2])

    # Push the new result type to the stack
    operand_type_stack.append(result_type)

    temp_var = globals.quadruples_queue.new_temp()
    globals.quadruples_queue.add_quadruple(p[2], p[1], p[3], temp_var)
    p[0] = temp_var

def p_exp_factor(p):
    "exp : termino"

    p[0] = p[1]

def p_termino(p):
    """termino : termino TIMES termino
                | termino DIVIDE termino"""

    # Pop the last types
    right_operand_type = operand_type_stack.pop()
    left_operand_type = operand_type_stack.pop()

    # Check expected type
    result_type = get_expected_type(left_operand_type, right_operand_type, p[2])

    # Push the new result type to the stack
    operand_type_stack.append(result_type)

    temp_var = globals.quadruples_queue.new_temp()
    globals.quadruples_queue.add_quadruple(p[2], p[1], p[3], temp_var)
    p[0] = temp_var

def p_termino_factor(p):
    "termino : factor"
    p[0] = p[1]

def p_factor(p):
    """factor : LPAREN expresion RPAREN
                | PLUS factor %prec UPLUS
                | MINUS factor %prec UMINUS
                | factor_opt"""

    if len(p) == 4:
        p[0] = p[2]
    elif len(p) == 3:
        if p[1] == '-':
            p[0] = -p[2]
        else:
            p[0] = p[2]
    else:
        p[0] = p[1]

def p_factor_opt(p):
    """factor_opt : cte
                    | ID"""

    # Get operand type if it exist in our vars table
    operand_type = get_operand_type(p[1])

    # Add it to the operand stack to keep track
    operand_type_stack.append(operand_type)

    p[0] = p[1]

def p_cte(p):
    """cte : CTEINT
            | CTEFLOAT
            | CTEBOOL"""
    p[0] = p[1]

def p_condition(p):
    "condition : condition_start body else_block ENDINSTRUC"

    # When we finish get the end jump index
    end_index = jump_stack.pop()

    # Add the pending index to the quadruple
    globals.quadruples_queue.edit_quadruple(end_index, None, None, None, globals.quadruples_queue.quadruples_len() + 1)

    p[0] = ['if', p[1], p[2], p[3]]

def p_condition_start(p):
    "condition_start : IF LPAREN expresion RPAREN"

    # Add the goto f when we finish evaluating the expression and save the index to return later
    globals.quadruples_queue.add_quadruple("gotof", p[3], None, None)
    jump_stack.append(globals.quadruples_queue.quadruples_len() - 1)

    p[0] = [p[1], p[3]]

def p_else_block(p):
    """else_block : ELSE check_else_jump body
            | empty"""
    if len(p) == 4:
        p[0] = [p[1], p[3]]

def p_check_else_jump(p):
    "check_else_jump : empty"

    # Add the goto f when we finish evaluating the expression
    globals.quadruples_queue.add_quadruple("goto", None, None, None)

    # Get the index of gotof we had pending
    pending_gotof_index = jump_stack.pop()

    # Save the new index to return later
    jump_stack.append(globals.quadruples_queue.quadruples_len() - 1)

    # Update the pending quadruple
    globals.quadruples_queue.edit_quadruple(pending_gotof_index, None, None, None, globals.quadruples_queue.quadruples_len() + 1)

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

    for expr in p[3]:
        if isinstance(expr, tuple):
            expr_value = expr[0]
            globals.quadruples_queue.add_quadruple('print', None, None, expr_value)
        else:
            globals.quadruples_queue.add_quadruple('print', None, None, expr)

    p[0] = ('print', p[3])

def p_print_opt(p):
    """print_opt : expresion more_opt
                | CTESTRING more_opt"""

    p[0] = [p[1]] + p[2]

def p_more_opt(p):
    """more_opt : COMMA print_opt
                | empty"""
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = []

def p_empty(p):
    "empty :"
    pass

def p_error(p):
    print("Syntax error in input!", p)

# Initialize stacks
current_type_stack = deque() # Used to keep track of type of vars when storing them in directory
current_var_stack = deque() # Used to keep track of name of vars when storing them in directory
operand_type_stack = deque() # Used to keep track of the operand type when we have operations
jump_stack = deque()

# Build parser
parser = yacc.yacc(start="prog")
