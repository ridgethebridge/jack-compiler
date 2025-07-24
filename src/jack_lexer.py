
from token import *
from symbol_table import *
class Jack_Lexer:

    def __init__(self, file_name):
        try:
            with open(file_name,"r") as file:
                self.code = file.read();
        except:
            print(f"unable to open file {file_name}")
            exit()
        self.cur_line = 1
        self.line_pos = 1
        self.cursor = 0
        self.cur_token = None
        self.error_log = ""
        self.cur_file = file_name

    def capture_token(self,name):
        if name == None:
            self.cur_token = EOF
        elif name == "field":
            self.cur_token = FIELD
        elif name == "true":
            self.cur_token = TRUE
        elif name == "false":
            self.cur_token = FALSE
        elif name == "null":
            self.cur_token = NULL
        elif name == "this":
            self.cur_token = THIS
        elif name == "let":
            self.cur_token = LET
        elif name == "do":
            self.cur_token = DO
        elif name == "if":
            self.cur_token = IF
        elif name == "else":
            self.cur_token = ELSE
        elif name == "while":
            self.cur_token = WHILE
        elif name == "return":
            self.cur_token = RETURN
        elif name == "int":
            self.cur_token = INT
        elif name == "boolean":
            self.cur_token = BOOL
        elif name == "char":
            self.cur_token = CHAR
        elif name == "static":
            self.cur_token = STATIC
        elif name == "constructor":
            self.cur_token = CONSTRUCTOR
        elif name == "method":
            self.cur_token = METHOD
        elif name == "function":
            self.cur_token = FUNCTION
        elif name == "void":
            self.cur_token = VOID
        elif name == "class":
            self.cur_token = CLASS
        elif name == "var":
            self.cur_token = VAR
        elif name == "{":
            self.cur_token = LEFT_CURLY
        elif name == "}":
            self.cur_token = RIGHT_CURLY
        elif name == "(":
            self.cur_token = LEFT_PAREN
        elif name == ")":
            self.cur_token = RIGHT_PAREN
        elif name == ",":
            self.cur_token = COMMA
        elif name == ";":
            self.cur_token = SEMICOLON
        elif name == "[":
            self.cur_token = LEFT_BRACKET
        elif name == "]":
            self.cur_token = RIGHT_BRACKET
        elif name == ".":
            self.cur_token = DOT
        elif name == "+":
            self.cur_token = PLUS
        elif name == "-":
            self.cur_token = MINUS
        elif name == "*":
            self.cur_token = ASTERISK
        elif name == "/":
            self.cur_token = FORWARD_SLASH
        elif name == "&":
            self.cur_token = AMPERSAND
        elif name == "|":
            self.cur_token = VERT_BAR
        elif name == "<":
            self.cur_token = LESS_THAN
        elif name == ">":
            self.cur_token = GREATER_THAN
        elif name == "=":
            self.cur_token = EQUALS
        elif name == "~":
            self.cur_token = TILDE
        else:
            self.cur_token = Token(name)

    def skip_blanks(self):
        while self.has_next():
            c = self.code[self.cursor]
            #whitespace handling
            while c == " " or c == "\n" or c == "\t":
                self.cursor +=1
                self.line_pos+=1
                if c == "\n":
                    self.cur_line+=1
                    self.line_pos = 1
                if not self.has_next():
                    return
                c = self.code[self.cursor]
            # comments
            if c == "/":
                if self.has_next():
                    if self.code[self.cursor+1] == '/':
                        while self.has_next() and self.code[self.cursor] != '\n':
                            self.cursor+=1
                            self.line_pos+=1
                    elif self.code[self.cursor+1] =='*':
                        self.cursor+=2 #skips over intial *
                        while len(self.code) - self.cursor >=2 and self.code[self.cursor:self.cursor+2] != '*/':
                            if "\n" in self.code[self.cursor:self.cursor+2]:
                                self.cur_line+=1
                                self.line_pos=1
                            self.cursor+=1
                        self.cursor+=2 # skips over */
                    else:
                        return
            else:
                return

    def lex_next_token(self):
        self.skip_blanks()
        name = None
        #EOF condition
        if not self.has_next():
            self.capture_token(None)
            return
        start = self.cursor
        self.cursor +=1
        self.line_pos+=1
        if is_alphanumeric(self.code[start]):
            while self.has_next() and is_alphanumeric(self.code[self.cursor]):
                self.cursor +=1
                self.line_pos+=1
        elif self.code[start] == "\"":
            while self.has_next() and self.code[self.cursor] != "\"":
                if self.code[self.cursor] == "\n":
                    self.report_error(f"syntax error: \" is missing at end of string {self.code[start:self.cursor]}, reached newline instead\n")
                    break
                self.cursor+=1
                self.line_pos+=1
            if self.has_next(): #this is to catch quote if there is one
                self.cursor+=1
                self.line_pos+=1
            else:
                self.report_error(f"syntax error: \" is missing at end of string {self.code[start:self.cursor]}, reached EOF instead\n")
        self.capture_token(self.code[start:self.cursor])
        s = token_class_to_str(self.cur_token.token_class)
        return self.cur_token
        
    def peek_ahead(self,k):
        start = self.cursor
        saved_ln = self.cur_line
        saved_lp = self.line_pos
        saved_error  = self.error_log
        i = 0
        while i < k:
            self.lex_next_token()
            i+=1
        self.cursor = start
        self.cur_line = saved_ln
        self.line_pos = saved_lp
        self.error_log = saved_error
        return self.cur_token
        
    def lex_identifier(self):
        t = self.peek_ahead(1)
        if self.cur_token.token_type != Token_Type.IDENTIFIER:
            self.report_error(f"syntax error: identifier is expected not {self.cur_token.name}\n")
            return t
        return self.lex_next_token()

    def has_next(self):
        return len(self.code) - self.cursor > 0

    def lex_expected_tokens(self,tts):
        t = self.peek_ahead(1)
        if not(t.token_type in tts):
            self.report_error(f"syntax error:  expected {tts} not {self.cur_token.name}\n")
            return t
        return self.lex_next_token()

    def lex_type(self): 
        t = self.peek_ahead(1)
        if not(self.cur_token.token_type == Token_Type.INT or self.cur_token.token_type == Token_Type.CHAR or self.cur_token.token_type == Token_Type.BOOL or self.cur_token.token_type == Token_Type.IDENTIFIER):
            self.report_error(f"invalid type on line {self.cur_line}:{self.line_pos}\n")
            return t
        return self.lex_next_token()

    def report_error(self,error):
            self.error_log+=error
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"

