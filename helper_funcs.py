# Imports
import re
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

    # Logical operators
    globals.CUBO_SEMANTICO['bool']['bool']['and'] = 'bool'
    globals.CUBO_SEMANTICO['bool']['bool']['or'] = 'bool'

# ------------------------------------------------- Helper functions -------------------------------------------------

# Function that returns the expected type of an operation
def get_expected_type(left_operand, right_operand, operator):
    if globals.CUBO_SEMANTICO[left_operand][right_operand][operator]:
        return globals.CUBO_SEMANTICO[left_operand][right_operand][operator]
    else:
        raise TypeError(f"'{operator}' is not supported between instances of '{left_operand}' and '{right_operand}'")

# Function that checks the type of a given operand
def get_operand_type(operand):
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

def translate_operator_to_memory(operator):
    translated_operator = globals.global_memory.get_operator_memory(operator)
    return translated_operator

def translate_operand_to_memory(operand, operand_type):
    translated_operand = -1

    if operand is not None:
        if operand in globals.funcs_dir[globals.current_scope]["vars"]:
            if operand_type == "int":
                translated_operand = globals.global_memory.get_var_int(operand)
            elif operand_type == "float":
                translated_operand = globals.global_memory.get_var_float(operand)
            elif operand_type == "bool":
                translated_operand = globals.global_memory.get_var_bool(operand)
        elif isinstance(operand, str) and operand[0] == "t":
            if operand_type == "int":
                translated_operand = globals.global_memory.get_temp_int(operand)
            elif operand_type == "float":
                translated_operand = globals.global_memory.get_temp_float(operand)
            elif operand_type == "bool":
                translated_operand = globals.global_memory.get_temp_bool(operand)
            elif operand_type == "string":
                translated_operand = globals.global_memory.get_const_string(operand)
        else:
            if isinstance(operand, bool):
                translated_operand = globals.global_memory.get_const_bool(operand)
            elif isinstance(operand, int):
                translated_operand = globals.global_memory.get_const_int(operand)
            elif isinstance(operand, float):
                translated_operand = globals.global_memory.get_const_float(operand)

    return translated_operand

def translate_result_to_memory(result, result_type):
    translated_result = -1

    if result is not None:
        if result in globals.funcs_dir[globals.current_scope]["vars"]:
            if result_type is None:
                result_type = globals.funcs_dir[globals.current_scope]["vars"][result]

            if result_type == "int":
                translated_result = globals.global_memory.get_var_int(result)
            elif result_type == "float":
                translated_result = globals.global_memory.get_var_float(result)
            elif result_type == "bool":
                translated_result = globals.global_memory.get_var_bool(result)
        elif isinstance(result, str) and result[0] == "t":
            if result_type == "int":
                translated_result = globals.global_memory.get_temp_int(result)
            elif result_type == "float":
                translated_result = globals.global_memory.get_temp_float(result)
            elif result_type == "bool":
                translated_result = globals.global_memory.get_temp_bool(result)
            elif result_type == "string":
                translated_result = globals.global_memory.get_const_string(result)
        else:
            if re.match(r'"([^"]*)"', result):
                translated_result = globals.global_memory.get_const_string(result)
            elif isinstance(result, bool):
                translated_result = globals.global_memory.get_const_bool(result)
            elif isinstance(result, int):
                translated_result = globals.global_memory.get_const_int(result)
            elif isinstance(result, float):
                translated_result = globals.global_memory.get_const_float(result)

    return translated_result

def translate_to_memory(operator, operand1, operand1_type, operand2, operand2_type, result, result_type):
    operator_memory = translate_operator_to_memory(operator)

    operand1_memory = translate_operand_to_memory(operand1, operand1_type)

    operand2_memory = translate_operand_to_memory(operand2, operand2_type)

    result_memory = translate_result_to_memory(result, result_type)

    return operator_memory, operand1_memory, operand2_memory, result_memory