# Imports
import globals

# Class to define a quadruple
class Quadruples:
    def __init__(self, operator, operand1=None, operand2=None, result=None):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.result = result

    def __repr__(self):
        return f"({self.operator}, {self.operand1}, {self.operand2}, {self.result})"

    def __str__(self):
        return f"({self.operator}, {self.operand1}, {self.operand2}, {self.result})"

# Class to generate the quadruples queue
class QuadruplesQueue:
    def __init__(self):
        self.quadruples_queue = []
        self.memory_quadruples_queue = []
        self.temp_count = 1

    def add_quadruple(self, operator, operand1=None, operand2=None, result=None):
        quad = Quadruples(operator, operand1, operand2, result)
        self.quadruples_queue.append(quad)
        return quad

    def add_memory_quadruple(self, operator, operand1=None, operand2=None, result=None):
        quad = Quadruples(operator, operand1, operand2, result)
        self.memory_quadruples_queue.append(quad)
        return quad

    def new_temp(self):
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def print_quadruples(self):
        for index, quad in enumerate(self.quadruples_queue):
            print(f"{index + 1}: {quad}")

    def print_memory_quadruples(self):
        for index, quad in enumerate(self.memory_quadruples_queue):
            print(f"{index + 1}: {quad}")

    def quadruples_len(self):
        return len(self.quadruples_queue)

    def edit_quadruple(self, index, operator=None, operand1=None, operand2=None, result=None):
        if 0 <= index < len(self.quadruples_queue):
            quad = self.quadruples_queue[index]
            if operator is not None:
                quad.operator = operator
            if operand1 is not None:
                quad.operand1 = operand1
            if operand2 is not None:
                quad.operand2 = operand2
            if result is not None:
                quad.result = result
        else:
            raise IndexError(f"Quadruple index {index} out of range")

    def edit_memory_quadruple(self, index, operator=None, operand1=None, operand2=None, result=None):
        if 0 <= index < len(self.memory_quadruples_queue):
            quad = self.memory_quadruples_queue[index]
            if operator is not None:
                quad.operator = operator
            if operand1 is not None:
                quad.operand1 = operand1
            if operand2 is not None:
                quad.operand2 = operand2
            if result is not None:
                quad.result = result
        else:
            raise IndexError(f"Quadruple index {index} out of range")

    def generate_obj_file(self):
        with open("ovejota.txt", "w") as file:
            # Operations array
            file.write("Operators/Operations:\n")
            file.write(f"{globals.global_memory.operators_operations_list}\n")

            # Global vars count and base
            file.write("Global vars:\n")
            file.write(f"Global int vars = {len(globals.global_memory.vars_int_list)}\n")
            file.write(f"base = {globals.global_memory.vars_int_base}\n")

            file.write(f"Global float vars = {len(globals.global_memory.vars_float_list)}\n")
            file.write(f"base = {globals.global_memory.vars_float_base}\n")

            file.write(f"Global bool vars = {len(globals.global_memory.vars_bool_list)}\n")
            file.write(f"base = {globals.global_memory.vars_bool_base}\n")

            # Temp vars count and base
            file.write("Tem vars:\n")
            file.write(f"Temp int vars = {len(globals.global_memory.temp_int_list)}\n")
            file.write(f"base = {globals.global_memory.temp_int_base}\n")

            file.write(f"Temp float vars = {len(globals.global_memory.temp_float_list)}\n")
            file.write(f"base = {globals.global_memory.temp_float_base}\n")

            file.write(f"Temp bool vars = {len(globals.global_memory.temp_bool_list)}\n")
            file.write(f"base = {globals.global_memory.temp_bool_base}\n")

            # Constants
            file.write("Constant integers:\n")
            file.write(f"base = {globals.global_memory.const_int_base}\n")
            file.write(f"{globals.global_memory.const_int_list}\n")

            file.write("Constant floats:\n")
            file.write(f"base = {globals.global_memory.const_float_base}\n")
            file.write(f"{globals.global_memory.const_float_list}\n")

            file.write("Constant strings:\n")
            file.write(f"base = {globals.global_memory.const_string_base}\n")
            file.write(f"{globals.global_memory.const_string_list}\n")

            file.write("Constant bools:\n")
            file.write(f"base = {globals.global_memory.const_bool_base}\n")
            file.write(f"{globals.global_memory.const_bool_list}\n")

            file.write("Quadruples list:\n")
            for quad in self.memory_quadruples_queue:
                file.write(f"{quad}\n")
