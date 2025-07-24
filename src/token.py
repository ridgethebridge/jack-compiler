
#TODO fix naming of tokens
from enum import Enum

def is_alphanumeric(c):
    return (c >="0" and c<="9") or (c >="A" and c <="Z") or (c >="a" and c <="z") or c =="_"

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

def is_number(token):
    for c in token:
        if not (c >="0" and c <="9"):
            return False
    return True

def is_identifier(token):
    if token[0] >="A" and token[0] <="Z" or token[0]>="a" and token[0]<="z" or token[0]=="_":
        for c in token[1:]:
            if not is_alphanumeric(c):
                return False
        return True
    return False
    

class Token:
    def __init__(self,name,t_class=None,t_type=None):
        if t_class == None or t_type == None:
            self.name = name
            if is_identifier(name):
                self.token_class = Token_Class.IDENTIFIER
                self.token_type = Token_Type.IDENTIFIER
            elif is_number(name):
                self.token_class = Token_Class.INT_CONSTANT
                self.token_type = Token_Type.INT_CONSTANT
            elif name[0] == "\"" and name[len(name)-1] == "\"": #fix definition
                self.token_class = Token_Class.STRING_CONSTANT
                self.token_type = Token_Type.STRING_CONSTANT
                self.name = name[1:len(name)-1] # fix
            else :
                self.token_class = Token_Class.INVALID
                self.token_type = Token_Type.INVALID
        else:
            self.name = name
            self.token_class = t_class
            self.token_type = t_type

    def __str__(self):
        return f"{self.name} {self.token_class} {self.token_type}"

#token constants
class Token_Class(Enum):
    KEYWORD = 0
    IDENTIFIER = 1
    INT_CONSTANT = 2
    STRING_CONSTANT = 3
    SYMBOL = 4
    OPERATOR = 5 # maybe get rid of
    INVALID = 6
    EOF = 7

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
    EOF = 44

#token constants
EOF = Token("EOF",Token_Class.EOF,Token_Type.EOF)
FIELD=Token("field",Token_Class.KEYWORD,Token_Type.FIELD)
TRUE=Token("true",Token_Class.KEYWORD,Token_Type.TRUE)
FALSE=Token("false",Token_Class.KEYWORD,Token_Type.FALSE)
NULL=Token("null",Token_Class.KEYWORD,Token_Type.NULL)
THIS=Token("this",Token_Class.KEYWORD,Token_Type.THIS)
LET=Token("let",Token_Class.KEYWORD,Token_Type.LET)
DO=Token("do",Token_Class.KEYWORD,Token_Type.DO)
IF=Token("if",Token_Class.KEYWORD,Token_Type.IF)
ELSE=Token("else",Token_Class.KEYWORD,Token_Type.ELSE)
WHILE=Token("while",Token_Class.KEYWORD,Token_Type.WHILE)
RETURN=Token("return",Token_Class.KEYWORD,Token_Type.RETURN)
INT=Token("int",Token_Class.KEYWORD,Token_Type.INT)
BOOL=Token("boolean",Token_Class.KEYWORD,Token_Type.BOOL)
CHAR=Token("char",Token_Class.KEYWORD,Token_Type.CHAR)
STATIC=Token("static",Token_Class.KEYWORD,Token_Type.STATIC)
CONSTRUCTOR=Token("constructor",Token_Class.KEYWORD,Token_Type.CONSTRUCTOR)
METHOD=Token("method",Token_Class.KEYWORD,Token_Type.METHOD)
FUNCTION=Token("function",Token_Class.KEYWORD,Token_Type.FUNCTION)
VOID=Token("void",Token_Class.KEYWORD,Token_Type.VOID)
CLASS=Token("class",Token_Class.KEYWORD,Token_Type.CLASS)
VAR=Token("var",Token_Class.KEYWORD,Token_Type.VAR)
LEFT_CURLY=Token("{",Token_Class.SYMBOL,Token_Type.LEFT_CURLY)
RIGHT_CURLY=Token("}",Token_Class.SYMBOL,Token_Type.RIGHT_CURLY)
LEFT_PAREN=Token("(",Token_Class.SYMBOL,Token_Type.LEFT_PAREN)
RIGHT_PAREN=Token(")",Token_Class.SYMBOL,Token_Type.RIGHT_PAREN)
COMMA=Token(",",Token_Class.SYMBOL,Token_Type.COMMA)
SEMICOLON=Token(";",Token_Class.SYMBOL,Token_Type.SEMICOLON)
LEFT_BRACKET=Token("[",Token_Class.SYMBOL,Token_Type.LEFT_BRACKET)
RIGHT_BRACKET=Token("]",Token_Class.SYMBOL,Token_Type.RIGHT_BRACKET)
DOT=Token(".",Token_Class.SYMBOL,Token_Type.DOT)
PLUS=Token("+",Token_Class.OPERATOR,Token_Type.PLUS)
MINUS=Token("-",Token_Class.OPERATOR,Token_Type.MINUS)
ASTERISK=Token("*",Token_Class.OPERATOR,Token_Type.ASTERISK)
FORWARD_SLASH=Token("/",Token_Class.OPERATOR,Token_Type.FORWARD_SLASH)
AMPERSAND=Token("&",Token_Class.OPERATOR,Token_Type.AMPERSAND)
VERT_BAR=Token("|",Token_Class.OPERATOR,Token_Type.VERT_BAR)
LESS_THAN=Token("<",Token_Class.OPERATOR,Token_Type.LESS_THAN)
GREATER_THAN=Token(">",Token_Class.OPERATOR,Token_Type.GREATER_THAN)
EQUALS=Token("=",Token_Class.OPERATOR,Token_Type.EQUALS)
TILDE=Token("~",Token_Class.SYMBOL,Token_Type.TILDE)

