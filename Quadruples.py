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

# Class to generate the quadruples queue
class QuadruplesQueue:
    def __init__(self):
        self.quadruples_queue = Queue()
        self.temp_count = 0

    def add_quadruple(self, operator, operand1=None, operand2=None, result=None):
        quad = Quadruples(operator, operand1, operand2, result)
        self.quadruples_queue.put(quad)
        return quad

    def new_temp(self):
        temp_name = f"t{self.temp_count}"
        self.temp_count += 1
        return temp_name

    def print_quadruples(self):
        for quad in self.quadruples:
            print(quad)