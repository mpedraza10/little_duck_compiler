class Memory:
    def __init__(self):
        # Base addresses for different types and scopes
        self.vars_int_base = 1000
        self.vars_float_base = 2000
        self.vars_bool_base = 3000
        self.const_int_base = 4000
        self.const_float_base = 5000
        self.const_string_base = 6000
        self.const_bool_base = 7000
        self.temp_int_base = 8000
        self.temp_float_base = 9000
        self.temp_bool_base = 10000

        # Operators/operations list
        self.operators_operations_list = ["+", "-", "*", "/", "=", ">", "<", "!=", "goto", "gotot", "gotof", "print"]

        # Lists to map variables
        self.vars_int_list = []
        self.vars_float_list = []
        self.vars_bool_list = []

        self.const_int_list = []
        self.const_float_list = []
        self.const_string_list = []
        self.const_bool_list = []

        self.temp_int_list = []
        self.temp_float_list = []
        self.temp_bool_list = []

    def allocate_var(self, var_name, var_type):
        if var_type == 'int':
            # Set the var considering the base
            self.vars_int_list.append(var_name)
        elif var_type == 'float':
            # Set the var considering the base
            self.vars_float_list.append(var_name)
        elif var_type == 'bool':
            # Set the var considering the base
            self.vars_bool_list.append(var_name)
        else:
            raise TypeError(f"Unknown variable type: {var_type}")

    def allocate_constant(self, value, var_type):
        if var_type == 'int':
            # Set the var considering the base
            self.const_int_list.append(value)
        elif var_type == 'float':
            # Set the var considering the base
            self.const_float_list.append(value)
        elif var_type == 'string':
            # Set the var considering the base
            self.const_string_list.append(value)
        elif var_type == 'bool':
            # Set the var considering the base
            self.const_bool_list.append(value)
        else:
            raise TypeError(f"Unknown variable type: {var_type}")

    def allocate_temp(self, temp, var_type):
        if var_type == 'int':
            # Set the var considering the base
            self.temp_int_list.append(temp)
        elif var_type == 'float':
            # Set the var considering the base
            self.temp_float_list.append(temp)
        elif var_type == 'bool':
            # Set the var considering the base
            self.temp_bool_list.append(temp)
        else:
            raise TypeError(f"Unknown variable type: {var_type}")

    def get_operator_memory(self, operator):
        try:
            index = self.operators_operations_list.index(operator)
            return index + 1
        except ValueError:
            print(f"{operator} is not in the list")

    def get_var_int(self, operand):
        try:
            index = self.vars_int_list.index(operand)
            return index + self.vars_int_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_var_float(self, operand):
        try:
            index = self.vars_float_list.index(operand)
            return index + self.vars_float_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_var_bool(self, operand):
        try:
            index = self.vars_bool_list.index(operand)
            return index + self.vars_bool_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_temp_int(self, operand):
        try:
            index = self.temp_int_list.index(operand)
            return index + self.temp_int_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_temp_float(self, operand):
        try:
            index = self.temp_float_list.index(operand)
            return index + self.temp_float_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_temp_bool(self, operand):
        try:
            index = self.temp_bool_list.index(operand)
            return index + self.temp_bool_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_const_bool(self, operand):
        try:
            index = self.const_bool_list.index(operand)
            return index + self.const_bool_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_const_int(self, operand):
        try:
            index = self.const_int_list.index(operand)
            return index + self.const_int_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_const_float(self, operand):
        try:
            index = self.const_float_list.index(operand)
            return index + self.const_float_base
        except ValueError:
            print(f"{operand} is not in the list")

    def get_const_string(self, operand):
        try:
            index = self.const_string_list.index(operand)
            return index + self.const_string_base
        except ValueError:
            print(f"{operand} is not in the list")

    def print_all_lists(self):
        list_titles = [
            "Integer vars",
            "Float vars",
            "Bool vars",
            "Const integers",
            "Const floats",
            "Const strings",
            "Const bool",
            "Temp int",
            "Temp float",
            "Temp bool"
        ]
        bases = [
            self.vars_int_base,
            self.vars_float_base,
            self.vars_bool_base,
            self.const_int_base,
            self.const_float_base,
            self.const_string_base,
            self.const_bool_base,
            self.temp_int_base,
            self.temp_float_base,
            self.temp_bool_base
        ]
        all_lists = [
            self.vars_int_list,
            self.vars_float_list,
            self.vars_bool_list,
            self.const_int_list,
            self.const_float_list,
            self.const_string_list,
            self.const_bool_list,
            self.temp_int_list,
            self.temp_float_list,
            self.temp_bool_list
        ]

        for i in range(len(all_lists)):
            current_list = all_lists[i]
            current_base = bases[i]
            current_title = list_titles[i]

            print(f"---------------------- {current_title} ----------------------")
            for i in range(len(current_list)):
                print(f"Address: {i + current_base} | Value: {current_list[i]}")
                print()
            print("--------------------------------------------------------------")
