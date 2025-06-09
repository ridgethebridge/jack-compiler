
from jack_lexer import *
from token import *
from sys import argv
import os
def main():
    if len(argv) < 2:
        print("must supply either file or directory!")
        exit()

    file = argv[1]
    if os.path.isdir(file):
        file = os.listdir(file)
    for f in file:
        if ".jack" in f:
            lexer = Jack_Lexer(f)
            lexer.lex_class_def()
            if lexer.error_log != "":
                print(lexer.error_log)
                exit()
            lexer.dump_xml_to_file(f.replace(".jack",".xml"))
main()

