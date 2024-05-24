# Imports
from quadruples_manager import QuadruplesQueue
from virtual_memory_assigner import VirtualMemoryCompiler

# Dictionary of functions and variables
funcs_dir = {
    'global': {
        'vars': {}
    }
}

# Current scope of the program
current_scope = 'global'

# Semantic cube
CUBO_SEMANTICO = {}

# Quadruplets queue
quadruples_queue = QuadruplesQueue() # Used to keep track of the generated quadruplets order

# Memory instance
global_memory = VirtualMemoryCompiler()