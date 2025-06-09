
#TODO list
#try to make making the xml file more efficient, maybe allocate larger buffer initially
# so new string isn't made every time a token is lexed

from token import *
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
        self.tree = "" # change way to do it
        self.cur_token = Token()
        self.error_log = ""
        self.cur_file = file_name

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
                        while len(self.code) - self.cursor >=2 and self.code[self.cursor:self.cursor+2] != '*/':
                            if "\n" in self.code[self.cursor:self.cursor+2]:
                                self.cur_line+=1
                                self.line_pos=1
                            self.cursor+=2
                        self.cursor=self.cursor+2 #skips over */
                    else:
                        return
            else:
                return

    def lex_next_token(self):
        self.skip_blanks()
        name = None
        #EOF condition
        if not self.has_next():
            self.cur_token.capture_token(None)
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
                    self.error_log+=f"syntax error: \" is missing at end of string {self.code[start:self.cursor]}, reached newline instead\n"
                    self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
                    break
                self.cursor+=1
                self.line_pos+=1
            if self.has_next(): #this is to catch quote if there is one
                self.cursor+=1
                self.line_pos+=1
            else:
                self.error_log+=f"syntax error: \" is missing at end of string {self.code[start:self.cursor]}, reached EOF instead\n"
                self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
        self.cur_token.capture_token(self.code[start:self.cursor])
        
        s = token_class_to_str(self.cur_token.token_class)
        self.tree += f"<{s}> {self.cur_token.name} </{s}>\n"

    def lex_class_var_dec(self): # fix so it parses comma separated declarations
        self.tree+="<classVarDec>\n"
        self.lex_next_token() 
        if self.cur_token.token_type != Token_Type.FIELD and self.cur_token.token_type != Token_Type.STATIC:
            self.error_log+=f"syntax error: field or static expected, not {self.cur_token.name}\n" 
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
        self.lex_type()
        while True:
            self.lex_identifier()
            self.lex_next_token()
            if self.cur_token.token_type == Token_Type.SEMICOLON:
               break
            elif self.cur_token.token_type == Token_Type.COMMA:
               pass
            else:
                self.error_log+=f"syntax error: semicolon expected to end declaration, not {self.cur_token.name}\n"
                self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
        self.tree+="</classVarDec>\n"

    
    #original grammar doesnt allow for alternating var decs and subroutine defs
    def lex_class_def(self): 
        self.tree+="<class>\n"
        self.lex_expected_token(Token_Type.CLASS)
        self.lex_identifier()
        self.lex_expected_token(Token_Type.LEFT_CURLY)
        #for var decs
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.STATIC or self.cur_token.token_type == Token_Type.FIELD:
                self.lex_class_var_dec()
            else:
                break
        #for function defs
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.FUNCTION or self.cur_token.token_type == Token_Type.METHOD or self.cur_token.token_type == Token_Type.CONSTRUCTOR:
                self.lex_subroutine_dec()
            else:
                break
        self.lex_expected_token(Token_Type.RIGHT_CURLY)
        self.tree+="</class>\n"
        
    def peek_ahead(self,k):
        saved_tree_state = self.tree
        start = self.cursor
        saved_ln = self.cur_line
        saved_lp = self.line_pos
        i = 0
        while i < k:
            self.lex_next_token()
            i+=1
        self.cursor = start
        self.tree = saved_tree_state
        self.cur_line = saved_ln
        self.line_pos = saved_lp
        
    def lex_subroutine_dec(self): 
        self.tree+="<subroutineDec>\n"
        self.lex_next_token()
        if not(self.cur_token.token_type == Token_Type.FUNCTION or self.cur_token.token_type == Token_Type.METHOD or self.cur_token.token_type == Token_Type.CONSTRUCTOR):
            self.error_log+=f"syntax error: keywords function, method, or constructor expected, not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
        self.peek_ahead(1)
        if self.cur_token.token_type == Token_Type.VOID:
             self.lex_next_token()
        else:
            self.lex_type() 
        self.lex_identifier()
        self.lex_expected_token(Token_Type.LEFT_PAREN)
        self.lex_parameter_list() 
        self.lex_expected_token(Token_Type.RIGHT_PAREN)
        self.lex_subroutine_body() 
        self.tree+="</subroutineDec>\n"

    def lex_subroutine_body(self): 
        self.tree+="<subroutineBody>\n"
        self.lex_expected_token(Token_Type.LEFT_CURLY)
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.VAR:
                self.lex_var_dec()
            else:
                break
        self.lex_multiple_statements()
        self.lex_expected_token(Token_Type.RIGHT_CURLY) #reads right curly
        self.tree+="</subroutineBody>\n"

    def lex_parameter_list(self): 
        self.tree+="<parameterList>\n"
        self.peek_ahead(1)
        if self.cur_token.token_type != Token_Type.RIGHT_PAREN:
            self.lex_type()
            self.lex_identifier()
            self.peek_ahead(1)
            while self.cur_token.token_type == Token_Type.COMMA:
                self.lex_next_token() # reads comma
                self.lex_type()
                self.lex_identifier()
                self.peek_ahead(1) #checks for comma again
        self.tree+="</parameterList>\n"

    def lex_var_dec(self): 
        self.tree+="<varDec>\n"
        self.lex_expected_token(Token_Type.VAR)
        self.lex_type()
        while True:
            self.lex_identifier()
            self.lex_next_token()
            if self.cur_token.token_type == Token_Type.COMMA:
                pass
            elif self.cur_token.token_type == Token_Type.SEMICOLON:
                break
            else:
                self.error_log+=f"syntax error: semicolon is expected to end variable declarations, not {self.cur_token.name}\n"
                self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
        self.tree+="</varDec>\n"

    def lex_type(self): 
        self.lex_next_token()
        if not(self.cur_token.token_type == Token_Type.INT or self.cur_token.token_type == Token_Type.CHAR or self.cur_token.token_type == Token_Type.BOOL or self.cur_token.token_type == Token_Type.IDENTIFIER):
            print("invalid type " + token.name)
            exit()

    #set of statement functions
    def lex_multiple_statements(self):
        self.tree+="<statements>\n"
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.RIGHT_CURLY:
                break
            self.lex_statement()
        self.tree+="</statements>\n"

    def lex_statement(self):
        self.peek_ahead(1)
        if self.cur_token.token_type == Token_Type.LET:
            self.lex_let_statement() 
        elif self.cur_token.token_type == Token_Type.IF: 
            self.lex_if_statement() 
        elif self.cur_token.token_type == Token_Type.WHILE: 
            self.lex_while_statement() 
        elif self.cur_token.token_type == Token_Type.DO: 
            self.lex_do_statement() 
        elif self.cur_token.token_type == Token_Type.RETURN: 
            self.lex_return_statement() 
        else:
            self.lex_next_token() #idk
            self.error_log+=f"syntax error: invalid statement, expecting do, let, if, while, or return keywords, not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"

    def lex_return_statement(self):
        self.tree+="<returnStatement>\n"
        self.lex_expected_token(Token_Type.RETURN)
        self.peek_ahead(1)
        if self.cur_token.token_type != Token_Type.SEMICOLON:
            self.lex_expression()
        self.lex_expected_token(Token_Type.SEMICOLON)
        self.tree+="</returnStatement>\n"
        

    def lex_do_statement(self):
        self.tree+="<doStatement>\n"
        self.lex_expected_token(Token_Type.DO)
        self.lex_subroutine_call()
        self.lex_expected_token(Token_Type.SEMICOLON)
        self.tree+="</doStatement>\n"
    
    def lex_while_statement(self):
        self.tree+="<whileStatement>\n"
        self.lex_expected_token(Token_Type.WHILE)
        self.lex_expected_token(Token_Type.LEFT_PAREN)
        self.lex_expression()
        self.lex_expected_token(Token_Type.RIGHT_PAREN)
        self.lex_expected_token(Token_Type.LEFT_CURLY)
        self.lex_multiple_statements()
        self.lex_expected_token(Token_Type.RIGHT_CURLY)
        self.tree+="</whileStatement>\n"
        
        # add else statements
    def lex_if_statement(self):
        self.tree+="<ifStatement>\n"
        self.lex_expected_token(Token_Type.IF)
        self.lex_expected_token(Token_Type.LEFT_PAREN)
        self.lex_expression()
        self.lex_expected_token(Token_Type.RIGHT_PAREN)
        self.lex_expected_token(Token_Type.LEFT_CURLY)
        self.lex_multiple_statements()
        self.lex_expected_token(Token_Type.RIGHT_CURLY)
        self.peek_ahead(1)
        if self.cur_token.token_type == Token_Type.ELSE:
            self.lex_expected_token(Token_Type.ELSE)
            self.lex_expected_token(Token_Type.LEFT_CURLY)
            self.lex_multiple_statements()
            self.lex_expected_token(Token_Type.RIGHT_CURLY)
        self.tree+="</ifStatement>\n"

    def lex_let_statement(self):
        self.tree+="<letStatement>\n"
        self.lex_expected_token(Token_Type.LET)
        self.lex_identifier()
        self.peek_ahead(1)
        if self.cur_token.token_type == Token_Type.LEFT_BRACKET:
            self.lex_expected_token(Token_Type.LEFT_BRACKET)
            self.lex_expression() 
            self.lex_expected_token(Token_Type.RIGHT_BRACKET)
            self.lex_expected_token(Token_Type.EQUALS)
        else:
            self.lex_expected_token(Token_Type.EQUALS)
        self.lex_expression() 
        self.lex_expected_token(Token_Type.SEMICOLON)
        self.tree+="</letStatement>\n"

    #set of expression functions
    def lex_expression(self):
        self.tree+="<expression>\n"
        self.lex_term() 
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_class == Token_Class.OPERATOR:
                self.lex_next_token() #check for proper operator
                self.lex_term()
            else:
                break
        self.tree+="</expression>\n"

    #TODO find better way grouping terminal elements, very redundant if chain
    def lex_term(self):
        self.tree+="<term>\n"
        self.peek_ahead(1)
        if self.cur_token.token_type == Token_Type.INT_CONSTANT:
           self.lex_next_token()
        elif self.cur_token.token_type == Token_Type.STRING_CONSTANT: 
           self.lex_next_token()
        elif self.cur_token.token_type == Token_Type.TRUE: 
            self.lex_next_token()
        elif self.cur_token.token_type == Token_Type.FALSE: 
            self.lex_next_token()
        elif self.cur_token.token_type == Token_Type.NULL: 
            self.lex_next_token()
        elif self.cur_token.token_type == Token_Type.THIS: 
            self.lex_next_token()
        elif self.cur_token.token_type == Token_Type.LEFT_PAREN:
            self.lex_expression()
            self.lex_expected_token(Token_Type.RIGHT_PAREN)
        elif self.cur_token.token_type == Token_Type.MINUS or self.cur_token.token_type == Token_Type.TILDE:
            self.lex_next_token() # maybe make a function for it?
            self.lex_term()
        elif self.cur_token.token_type == Token_Type.IDENTIFIER:
            self.peek_ahead(2)
            if self.cur_token.token_type == Token_Type.LEFT_BRACKET:
                self.lex_identifier() #reads name
                self.lex_next_token() # reads left bracket
                self.lex_expression()
                self.lex_expected_token(Token_Type.RIGHT_BRACKET)
            elif self.cur_token.token_type == Token_Type.LEFT_PAREN or self.cur_token.token_type == Token_Type.DOT:
                self.lex_subroutine_call() 
            else:
                self.lex_identifier()
        else:
            self.error_log+=f"syntax error: invalid term for expression, type or expression expected, not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
        self.tree+="</term>\n"

    def lex_subroutine_call(self):
        self.lex_identifier()
        self.lex_next_token()
        if self.cur_token.token_type == Token_Type.DOT:
            self.lex_identifier()
            self.lex_expected_token(Token_Type.LEFT_PAREN)
        elif self.cur_token.token_type != Token_Type.LEFT_PAREN:
            self.error_log+=f"syntax error: ( is expected for subroutine call not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
        self.lex_expression_list()
        self.lex_expected_token(Token_Type.RIGHT_PAREN)

    def lex_expression_list(self):
        self.tree+="<expressionList>\n"
        self.peek_ahead(1)
        while self.cur_token.token_type != Token_Type.RIGHT_PAREN:
            self.lex_expression()
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.COMMA:
                self.lex_next_token()
        self.tree+="</expressionList>\n"


    def lex_identifier(self):
        self.lex_next_token()
        if self.cur_token.token_type != Token_Type.IDENTIFIER:
            self.error_log+=f"syntax error: identifier is expected not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"

    def has_next(self):
        return len(self.code) - self.cursor > 0

    def dump_xml_to_file(self,file_name):
        try:
            with open(file_name,"w") as file:
                file.write(self.tree)
        except:
            print("could not open file for writing")
            exit()

    def lex_expected_token(self,tt):
        self.lex_next_token()
        if self.cur_token.token_type != tt:
            self.error_log+=f"syntax error:  expected {tt} not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
    
