
from jack_lexer import *
from token import *
from sys import argv
from xml_generator import *
import os
def main():
    if len(argv) < 2:
        print("must supply either file or directory!")
        exit()

    file = argv[1]
    if os.path.isdir(file):
        file = os.listdir(file)
    else:
        file = [file]
    for f in file:
        if ".jack" in f:
            lexer = Jack_Lexer(f)
            tree = compile_class(lexer)
            if lexer.error_log != "":
                print(lexer.error_log)
                exit()
            dump_xml_to_file(tree,f.replace(".jack",".xml"))
main()

