
#TODO
#fix how tokens are named
from enum import Enum

def token_class_to_str(tc):
    if tc == Token_Class.IDENTIFIER:
        return "identifier"
    elif tc == Token_Class.KEYWORD:
        return "keyword"
    elif tc == Token_Class.SYMBOL or tc == Token_Class.OPERATOR:
        return "symbol"
    elif tc == Token_Class.INT_CONSTANT:
        return "integerConstant"
    elif tc == Token_Class.STRING_CONSTANT:
        return "stringConstant"

class Token:
    # so fucking bad
    def __init__(self):
        self.name = None
        self.token_class = None
        self.token_type = None


    def capture_token(self,name):
        self.name = name
        if name == "field":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.FIELD
        elif name == "true":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.TRUE
        elif name == "false":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.FALSE
        elif name == "null":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.NULL
        elif name == "this":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.THIS
        elif name == "let":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.LET
        elif name == "do":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.DO
        elif name == "if":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.IF
        elif name == "else":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.ELSE
        elif name == "while":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.WHILE
        elif name == "return":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.RETURN
        elif name == "int":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.INT
        elif name == "boolean":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.BOOL
        elif name == "char":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.CHAR
        elif name == "static":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.STATIC
        elif name == "constructor":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.CONSTRUCTOR
        elif name == "method":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.METHOD
        elif name == "function":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.FUNCTION
        elif name == "void":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.VOID
        elif name == "class":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.CLASS
        elif name == "var":
            self.token_class = Token_Class.KEYWORD
            self.token_type = Token_Type.VAR
        elif name == "{":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.LEFT_CURLY
        elif name == "}":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.RIGHT_CURLY
        elif name == "(":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.LEFT_PAREN
        elif name == ")":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.RIGHT_PAREN
        elif name == ",":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.COMMA
        elif name == ";":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.SEMICOLON
        elif name == "[":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.LEFT_BRACKET
        elif name == "]":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.RIGHT_BRACKET
        elif name == ".":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.DOT
        elif name == "+":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.PLUS
        elif name == "-":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.MINUS
        elif name == "*":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.ASTERISK
        elif name == "/":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.FORWARD_SLASH
        elif name == "&":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.AMPERSAND
        elif name == "|":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.VERT_BAR
        elif name == "<":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.LESS_THAN
            self.name = "&lt;"
        elif name == ">":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.GREATER_THAN
            self.name = "&gt;"
        elif name == "=":
            self.token_class = Token_Class.OPERATOR
            self.token_type = Token_Type.EQUALS
        elif name == "~":
            self.token_class = Token_Class.SYMBOL
            self.token_type = Token_Type.TILDE
        elif name[0] >= "A" and name[0] <="z": # should invalid on bad identifer
            self.token_class = Token_Class.IDENTIFIER
            self.token_type = Token_Type.IDENTIFIER
        elif name[0] >="0" and name[0] <="9": # should invalid on bad int constant
            self.token_class = Token_Class.INT_CONSTANT
            self.token_type = Token_Type.INT_CONSTANT
        elif name[0] == "\"" and name[len(name)-1] == "\"": #fix definition
            self.token_class = Token_Class.STRING_CONSTANT
            self.token_type = Token_Type.STRING_CONSTANT
            self.name = name[1:len(name)-1] # fix
        else :
            self.token_class = None
            self.token_type = Token_Type.INVALID

class Token_Class(Enum):
    KEYWORD = 0
    IDENTIFIER = 1
    INT_CONSTANT = 2
    STRING_CONSTANT = 3
    SYMBOL = 4
    OPERATOR = 5 # maybe get rid of

class Token_Type(Enum):
    FIELD = 0
    INT = 1
    IDENTIFIER = 2
    STATIC = 3
    BOOL = 4
    CHAR = 5
    CONSTRUCTOR = 6
    METHOD = 7
    FUNCTION = 8
    VOID = 9
    INT_CONSTANT = 10
    CLASS = 11
    LEFT_CURLY = 12
    RIGHT_CURLY = 13
    LEFT_PAREN =14
    RIGHT_PAREN = 15
    COMMA = 16
    INVALID = 17
    SEMICOLON = 18
    TRUE = 19
    FALSE = 20
    NULL = 21
    THIS = 22
    LET = 23
    DO = 24
    IF = 25
    ELSE = 26
    WHILE = 27
    RETURN = 28
    LEFT_BRACKET = 29
    RIGHT_BRACKET = 30
    DOT = 31
    PLUS = 32
    MINUS = 33
    ASTERISK = 34
    FORWARD_SLASH = 35
    AMPERSAND = 36
    VERT_BAR = 37
    LESS_THAN = 38
    GREATER_THAN = 39
    TILDE = 40
    STRING_CONSTANT = 41
    VAR = 42
    EQUALS = 43
