
from sys import argv
import os
from code_generator import *
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
            gen = Code_Generator(f)
            gen.compile_class()
            if len(gen.lexer.error_log) > 0:
                print(gen.lexer.error_log)
                exit()
            gen.dump_vm(f.replace("jack","vm"))
main()

