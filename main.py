# Imports
import os
from plylexer import lexer
from plyparser import parser
from virtual_machine import VirtualMachine
import globals
from helper_funcs import generate_cubo_semantico

if __name__ == "__main__":
    # Define the path to the input file
    input_file_path = os.path.join("tests", "BasicProgram.txt")

    # Read the content of the input file
    with open(input_file_path, "r") as file:
        data = file.read()

    # Generate the semantic cube
    generate_cubo_semantico()

    # Tokenize
    print("")
    print("-------------------------- Scanner --------------------------")
    print("")
    # Give the lexer some input
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break # No more input
        print(tok)
    print("")
    print("-------------------------------------------------------------")
    print("")

    print("")
    print("-------------------------- Parser --------------------------")
    print("")
    # Parse the input and get the results
    parse_tree = parser.parse(data, debug=True)
    print("Parse Tree: ", parse_tree)
    print("")
    print("------------------------------------------------------------")
    print("")

    print("")
    print("-------------------------- Function and vars directory --------------------------")
    print("")
    for key in globals.funcs_dir:
        print(key + ": ")
        print(globals.funcs_dir[key])
    print("")
    print("------------------------------------------------------------")
    print("")

    print("")
    print("-------------------------- Quadruplets queue --------------------------")
    print("")
    globals.quadruples_queue.print_quadruples()
    print("")
    print("------------------------------------------------------------")
    print("")

    print("")
    print("-------------------------- Memory addresses --------------------------")
    print("")
    globals.global_memory.print_all_lists()
    print("")
    print("------------------------------------------------------------")
    print("")

    print("")
    print("-------------------------- Quadruplets with memory addresses --------------------------")
    print("")
    globals.quadruples_queue.print_memory_quadruples()
    print("")
    print("------------------------------------------------------------")
    print("")

    # Generate txt file
    globals.quadruples_queue.generate_obj_file()

    # Start virtual machine
    vm = VirtualMachine("ovejota.txt")
    vm.execute()