class Memory:
    def __init__(self, int_space, float_space, bool_space, bases):
        # Bases for memory space
        self.int_base, self.float_base, self.bool_base = bases

        # List of vars memory spaces
        self.integers = [None] * int_space
        self.floats = [None] * float_space
        self.bools = [None] * bool_space