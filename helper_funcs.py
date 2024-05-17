# Imports
import globals

# ------------------------------------------------- Tabla de consideraciones semanticas (cubo semantico) -------------------------------------------------

def generate_cubo_semantico():
    # Definir los tipos y operadores
    tipos = ['int', 'float', 'bool']
    operadores = ['+', '-', '*', '/', '!=', '<', '>']

    # Inicializar el cubo semántico
    for tipo1 in tipos:
        globals.CUBO_SEMANTICO[tipo1] = {}
        for tipo2 in tipos:
            globals.CUBO_SEMANTICO[tipo1][tipo2] = {}
            for operador in operadores:
                globals.CUBO_SEMANTICO[tipo1][tipo2][operador] = None

    # Ejemplo de llenado del cubo semántico para algunos operadores
    globals.CUBO_SEMANTICO['int']['int']['+'] = 'int'
    globals.CUBO_SEMANTICO['int']['int']['-'] = 'int'
    globals.CUBO_SEMANTICO['int']['int']['*'] = 'int'
    globals.CUBO_SEMANTICO['int']['int']['/'] = 'float'

    globals.CUBO_SEMANTICO['float']['float']['+'] = 'float'
    globals.CUBO_SEMANTICO['float']['float']['-'] = 'float'
    globals.CUBO_SEMANTICO['float']['float']['*'] = 'float'
    globals.CUBO_SEMANTICO['float']['float']['/'] = 'float'

    globals.CUBO_SEMANTICO['int']['float']['+'] = 'float'
    globals.CUBO_SEMANTICO['float']['int']['+'] = 'float'
    globals.CUBO_SEMANTICO['int']['float']['-'] = 'float'
    globals.CUBO_SEMANTICO['float']['int']['-'] = 'float'
    globals.CUBO_SEMANTICO['int']['float']['-'] = 'float'
    globals.CUBO_SEMANTICO['float']['int']['-'] = 'float'
    globals.CUBO_SEMANTICO['int']['float']['*'] = 'float'
    globals.CUBO_SEMANTICO['float']['int']['*'] = 'float'
    globals.CUBO_SEMANTICO['int']['float']['/'] = 'float'
    globals.CUBO_SEMANTICO['float']['int']['/'] = 'float'

    # Ejemplo para operadores relacionales
    globals.CUBO_SEMANTICO['int']['int']['!='] = 'bool'
    globals.CUBO_SEMANTICO['int']['int']['<'] = 'bool'
    globals.CUBO_SEMANTICO['int']['int']['>'] = 'bool'

    globals.CUBO_SEMANTICO['float']['float']['!='] = 'bool'
    globals.CUBO_SEMANTICO['float']['float']['<'] = 'bool'
    globals.CUBO_SEMANTICO['float']['float']['>'] = 'bool'

    globals.CUBO_SEMANTICO['int']['float']['!='] = 'bool'
    globals.CUBO_SEMANTICO['float']['int']['!='] = 'bool'
    globals.CUBO_SEMANTICO['int']['float']['<'] = 'bool'
    globals.CUBO_SEMANTICO['float']['int']['<'] = 'bool'
    globals.CUBO_SEMANTICO['int']['float']['>'] = 'bool'
    globals.CUBO_SEMANTICO['float']['int']['>'] = 'bool'

# ------------------------------------------------- Helper functions -------------------------------------------------

# Function that returns the expected type of an operation
def get_expected_type(left_operand, right_operand, operator):
    if globals.CUBO_SEMANTICO[left_operand][right_operand][operator]:
        return globals.CUBO_SEMANTICO[left_operand][right_operand][operator]
    else:
        raise TypeError(f"'{operator}' is not supported between instances of '{left_operand}' and '{right_operand}'")

# Function that checks the type of a given operand
def get_operand_type(operand):
    # Get the global current scope
    #global globals.current_scope

    print("------------------------------- Current scope in get operand type in ", globals.current_scope)

    # Initialize the return var
    operand_type = ""

    # First check if we are not in global in order to also look into those variables
    if globals.current_scope != "global":
        # Check the types of the operands
        if operand in globals.funcs_dir[globals.current_scope]["vars"]:
            operand_type = globals.funcs_dir[globals.current_scope]["vars"][operand]
        elif operand in globals.funcs_dir["global"]["vars"]:
            operand_type = globals.funcs_dir["global"]["vars"][operand]
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
        if operand in globals.funcs_dir[globals.current_scope]["vars"]:
            operand_type = globals.funcs_dir[globals.current_scope]["vars"][operand]
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