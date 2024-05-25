# Program that simulates a computer that is responsible for reading the code and interpreting it.
# Both a processor and memory are simulated to roughly replicate the Von Neuman architecture.

# Imports
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

        for line in lines:
            line = line.strip()

            if line == "Operators/Operations:":
                reading_operators = True
                continue

            # Look for the global and temp parameters
            if line == "Global vars:":
                reading_operators = False
                reading_globals = True
                reading_temps = False
                continue
            if line == "Tem vars:":
                reading_globals = False
                reading_temps = True
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
                    if global_int_vars == 0:
                        global_int_base = int(line.split('=')[1].strip())
                    elif global_float_vars == 0:
                        global_float_base = int(line.split('=')[1].strip())
                    elif global_bool_vars == 0:
                        global_bool_base = int(line.split('=')[1].strip())
                elif "Global int vars" in line:
                    global_int_vars = int(line.split('=')[1].strip())
                elif "Global float vars" in line:
                    global_float_vars = int(line.split('=')[1].strip())
                elif "Global bool vars" in line:
                    global_bool_vars = int(line.split('=')[1].strip())
            elif reading_temps:
                if line.startswith("base ="):
                    if temp_int_vars == 0:
                        temp_int_base = int(line.split('=')[1].strip())
                    elif temp_float_vars == 0:
                        temp_float_base = int(line.split('=')[1].strip())
                    elif temp_bool_vars == 0:
                        temp_bool_base = int(line.split('=')[1].strip())
                elif "Temp int vars" in line:
                    temp_int_vars = int(line.split('=')[1].strip())
                elif "Temp float vars" in line:
                    temp_float_vars = int(line.split('=')[1].strip())
                elif "Temp bool vars" in line:
                    temp_bool_vars = int(line.split('=')[1].strip())
            elif reading_integers:
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

        # Finally create the const table
        const_table = {str(const_integers_base + i): v for i, v in enumerate(const_integers)}
        const_table.update({str(const_floats_base + i): v for i, v in enumerate(const_floats)})
        const_table.update({str(const_strings_base + i): v for i, v in enumerate(const_strings)})
        const_table.update({str(const_bools_base + i): v for i, v in enumerate(const_bools)})

        # Create all memory needed
        self.global_memory = Memory(global_int_vars, global_float_vars, global_bool_vars, [global_int_base, global_float_base, global_bool_base])
        self.temp_memory = Memory(temp_int_vars, temp_float_vars, temp_bool_vars, [temp_int_base, temp_float_base, temp_bool_base])

        print(self.operators_operations_list)

        return quadruples, const_table
