# Imports
from queue import Queue

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
        self.temp_count = 1

    def add_quadruple(self, operator, operand1=None, operand2=None, result=None):
        quad = Quadruples(operator, operand1, operand2, result)
        self.quadruples_queue.append(quad)
        return quad

    def new_temp(self):
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def print_quadruples(self):
        for index, quad in enumerate(self.quadruples_queue):
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
