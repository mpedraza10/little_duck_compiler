# Imports
import os
from plylexer import lexer
from plyparser import parser
from globals import funcs_dir
from helper_funcs import generate_cubo_semantico

if __name__ == "__main__":
    # Define the path to the input file
    input_file_path = os.path.join("tests", "QuadTest.txt")

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
    print("Function and Vars Directory: ")
    for key in funcs_dir:
        print(key + ": ")
        print(funcs_dir[key])
    print("")