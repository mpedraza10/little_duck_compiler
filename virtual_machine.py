# Program that simulates a computer that is responsible for reading the code and interpreting it.
# Both a processor and memory are simulated to roughly replicate the Von Neuman architecture.

# Imports
import gc
from vm_memory import Memory

class VirtualMachine:
    def __init__(self, obj_file):
        self.global_memory = None
        self.temp_memory = None
        self.local_memory = None
        self.instruction_pointer = 0
        self.operators_operations_list = None
        self.code_segment, self.const_table = self.load_obj_file(obj_file)

    def load_obj_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        # Constants
        const_integers_base = 0
        const_integers = []
        const_floats_base = 0
        const_floats = []
        const_strings_base = 0
        const_strings = []
        const_bools_base = 0
        const_bools = []

        # Quadruples
        quadruples = []

        # Global and Temp Variables
        global_int_vars = 0
        global_float_vars = 0
        global_bool_vars = 0
        temp_int_vars = 0
        temp_float_vars = 0
        temp_bool_vars = 0

        global_int_base = 0
        global_float_base = 0
        global_bool_base = 0
        temp_int_base = 0
        temp_float_base = 0
        temp_bool_base = 0

        # Flags for reading sections
        reading_operators = False
        reading_globals = False
        reading_temps = False
        reading_integers = False
        reading_floats = False
        reading_strings = False
        reading_bools = False

        # Var to store prev line in case we need it
        previous_line = None

        for line in lines:
            line = line.strip()

            if line == "Operators/Operations:":
                reading_operators = True
                reading_globals = False
                reading_temps = False
                reading_integers = False
                reading_floats = False
                reading_strings = False
                reading_bools = False
                continue

            # Look for the global and temp parameters
            if line == "Global vars:":
                reading_operators = False
                reading_globals = True
                reading_temps = False
                reading_integers = False
                reading_floats = False
                reading_strings = False
                reading_bools = False
                continue
            if line == "Tem vars:":
                reading_operators = False
                reading_globals = False
                reading_temps = True
                reading_integers = False
                reading_floats = False
                reading_strings = False
                reading_bools = False
                continue
            if line == "Constant integers:":
                reading_globals = False
                reading_temps = False
                reading_integers = True
                reading_floats = False
                reading_strings = False
                reading_bools = False
                continue
            if line == "Constant floats:":
                reading_integers = False
                reading_floats = True
                continue
            if line == "Constant strings:":
                reading_floats = False
                reading_strings = True
                continue
            if line == "Constant bools:":
                reading_strings = False
                reading_bools = True
                continue
            if line == "Quadruples list:":
                reading_bools = False
                continue

            if reading_operators:
                self.operators_operations_list = eval(line)

            if reading_globals:
                if line.startswith("base ="):
                    base_value = int(line.split('=')[1].strip())
                    if 'Global int vars' in previous_line:
                        global_int_base = base_value
                    elif 'Global float vars' in previous_line:
                        global_float_base = base_value
                    elif 'Global bool vars' in previous_line:
                        global_bool_base = base_value
                elif "Global int vars" in line:
                    global_int_vars = int(line.split('=')[1].strip())
                elif "Global float vars" in line:
                    global_float_vars = int(line.split('=')[1].strip())
                elif "Global bool vars" in line:
                    global_bool_vars = int(line.split('=')[1].strip())

            if reading_temps:
                if line.startswith("base ="):
                    base_value = int(line.split('=')[1].strip())
                    if 'Temp int vars' in previous_line:
                        temp_int_base = base_value
                    elif 'Temp float vars' in previous_line:
                        temp_float_base = base_value
                    elif 'Temp bool vars' in previous_line:
                        temp_bool_base = base_value
                elif "Temp int vars" in line:
                    temp_int_vars = int(line.split('=')[1].strip())
                elif "Temp float vars" in line:
                    temp_float_vars = int(line.split('=')[1].strip())
                elif "Temp bool vars" in line:
                    temp_bool_vars = int(line.split('=')[1].strip())

            if reading_integers:
                if line.startswith("base ="):
                    const_integers_base = int(line.split('=')[1].strip())
                else:
                    const_integers = eval(line)
            elif reading_floats:
                if line.startswith("base ="):
                    const_floats_base = int(line.split('=')[1].strip())
                else:
                    const_floats = eval(line)
            elif reading_strings:
                if line.startswith("base ="):
                    const_strings_base = int(line.split('=')[1].strip())
                else:
                    const_strings = eval(line)
            elif reading_bools:
                if line.startswith("base ="):
                    const_bools_base = int(line.split('=')[1].strip())
                else:
                    const_bools = eval(line)
            else:
                if line.startswith("("):
                    quadruples.append(list(map(int, eval(line))))

            previous_line = line

        # Parse constant strings to remove the ""
        formatted_const_strings = [None] * len(const_strings)
        for index, string in enumerate(const_strings):
            new_string = string[1:-1] if len(string) > 1 else ""
            formatted_const_strings[index] = new_string

        # Delete the prev string constants list
        del const_strings
        gc.collect()

        # Finally create the const table
        const_table = {const_integers_base + i: v for i, v in enumerate(const_integers)}
        const_table.update({const_floats_base + i: v for i, v in enumerate(const_floats)})
        const_table.update({const_strings_base + i: v for i, v in enumerate(formatted_const_strings)})
        const_table.update({const_bools_base + i: v for i, v in enumerate(const_bools)})

        # Create all memory needed
        self.global_memory = Memory(global_int_vars, global_float_vars, global_bool_vars, [global_int_base, global_float_base, global_bool_base])
        self.temp_memory = Memory(temp_int_vars, temp_float_vars, temp_bool_vars, [temp_int_base, temp_float_base, temp_bool_base])

        return quadruples, const_table

    def execute(self):
        while self.instruction_pointer < len(self.code_segment):
            current_quad = self.code_segment[self.instruction_pointer]
            self.handle_instruction(current_quad)
            self.instruction_pointer += 1

    def set_value(self, result_address, value):
        # Use the ranges of the bases to determine weather we're having a global or temp var and store the value
        if result_address >=  self.global_memory.int_base and result_address <= self.global_memory.bool_base + 999:
            if result_address >= self.global_memory.int_base and result_address < self.global_memory.float_base:
                self.global_memory.integers[result_address - self.global_memory.int_base] = value
            elif result_address >= self.global_memory.float_base and result_address < self.global_memory.bool_base:
                self.global_memory.floats[result_address - self.global_memory.float_base] = value
            else:
                self.global_memory.bools[result_address - self.global_memory.bool_base] = value
        else:
            if result_address >= self.temp_memory.int_base and result_address < self.temp_memory.float_base:
                self.temp_memory.integers[result_address - self.temp_memory.int_base] = value
            elif result_address >= self.temp_memory.float_base and result_address < self.temp_memory.bool_base:
                self.temp_memory.floats[result_address - self.temp_memory.float_base] = value
            elif result_address >= self.temp_memory.bool_base and result_address < self.temp_memory.bool_base + 999:
                self.temp_memory.bools[result_address - self.temp_memory.bool_base] = value
            else:
                raise MemoryError(f"Address {result_address} not available!")

    def get_value(self, operand):
        if operand in self.const_table:
            return self.const_table[operand]
        else:
            if operand >=  self.global_memory.int_base and operand <= self.global_memory.bool_base + 999:
                if operand >= self.global_memory.int_base and operand < self.global_memory.float_base:
                    return self.global_memory.integers[operand - self.global_memory.int_base]
                elif operand >= self.global_memory.float_base and operand < self.global_memory.bool_base:
                    return self.global_memory.floats[operand - self.global_memory.float_base]
                else:
                    return self.global_memory.bools[operand - self.global_memory.bool_base]
            else:
                if operand >= self.temp_memory.int_base and operand < self.temp_memory.float_base:
                    return self.temp_memory.integers[operand - self.temp_memory.int_base]
                elif operand >= self.temp_memory.float_base and operand < self.temp_memory.bool_base:
                    return self.temp_memory.floats[operand - self.temp_memory.float_base]
                elif operand >= self.temp_memory.bool_base and operand < self.temp_memory.bool_base + 999:
                    return self.temp_memory.bools[operand - self.temp_memory.bool_base]
                else:
                    raise MemoryError(f"Address {operand} not available!")


    def handle_instruction(self, instruction):
        # Get all components of the quadruple instruction
        operator, left_operand, right_operand, result = instruction

        # Check what operation are we doing and store results in memory
        if self.operators_operations_list[operator - 1] == "+":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val + right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "-":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val - right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "*":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val * right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "/":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val / right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "=":
            # Get values of operands
            left_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            # Do the operation
            res = left_val

            # Set right_val value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == ">":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val > right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "<":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val < right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "!=":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val != right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "goto":
            # Get the destination of where to move the pointer
            self.instruction_pointer = result - 2
        elif self.operators_operations_list[operator - 1] == "gotot":
            # Get values of operands
            left_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            # Get the destination of where to move the pointer
            if left_val:
                self.instruction_pointer = result - 2
        elif self.operators_operations_list[operator - 1] == "gotof":
            # Get values of operands
            left_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            # Get the destination of where to move the pointer
            if not left_val:
                self.instruction_pointer = result - 2
        elif self.operators_operations_list[operator - 1] == "print":
            res = self.get_value(result)
            print(res)
        elif self.operators_operations_list[operator - 1] == "and":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val and right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
        elif self.operators_operations_list[operator - 1] == "or":
            # Get values of operands
            left_val = None
            right_val = None
            if left_operand in self.const_table:
                left_val = self.const_table[left_operand]
            else:
                left_val = self.get_value(left_operand)

            if right_operand in self.const_table:
                right_val = self.const_table[right_operand]
            else:
                right_val = self.get_value(right_operand)

            # Do the operation
            res = left_val or right_val

            # Set the value in corresponding memory
            self.set_value(result, res)
