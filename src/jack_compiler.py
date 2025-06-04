
from jack_lexer import *
from token import *
def main():
    lexer = Jack_Lexer(input())
    lexer.lex_class_def()
    if lexer.error_log != "":
        print(lexer.error_log)
        exit()
    lexer.dump_xml_to_file(input())

main()

