
#TODO list
# make some error functions for certain types of errors like missing ;
#maybe do what tsoding does and have a expect_next_token
#try to make making the xml file more efficient, maybe allocate larger buffer initially
# so new string isn't made every time a token is lexed
#maybe make a lex_statements function to add statements token to tree
# if and while are similar in structure, maybe refactor to not repeat code

#important things
#overall add some slight changes to the grammar to make it fit my style
# the grammar allows for elements to be empty strings, maybe change this
# enforcing some values, it makes it difficult to determine how to end parsing functions
# empty strings also seem to hinder recursion

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

    def switch_file(self,file_name):
        with open(file_name,"r") as file:
            self.code = file.read()
        self.cur_line = 1
        self.line_pos = 1
        self.cursor = 0
        self.tree = ""

#fix so it works
    def skip_blanks(self):
        while self.has_next():
            c = self.code[self.cursor]
            while c == " " or c == "\n" or c == "\t":
                self.cursor +=1
                c = self.code[self.cursor]
            if c == "/":
                if self.has_next():
                    if self.code[self.cursor+1] == '/':
                        while self.has_next() and self.code[self.cursor] != '\n':
                            self.cursor+=1
                        self.cursor+=1 # skips over new line
                        if not self.has_next():
                            break
                    elif self.code[self.cursor+1] =='*':
                        while len(self.code) - self.cursor >=2 and self.code[self.cursor:self.cursor+2] != '*/':
                            self.cursor+=1
                            if not (len(self.code) - self.cursor >=2): # didnt read */ which i error
                                print("major error /* with no */ is eroor!!!")
                                break
                        self.cursor=self.cursor+2 #skips over */
                    else:
                        #in this case it is a fivision symbol
                        break
            else:
                break

    def lex_next_token(self):
        self.skip_blanks()
        name = None
        if not self.has_next():
            print("lexer error: end of line reached when token expected")
            exit()
        start = self.cursor
        self.cursor +=1
        if is_alphanumeric(self.code[start]):
            while self.has_next() and is_alphanumeric(self.code[self.cursor]):
                self.cursor +=1
            name = self.code[start:self.cursor]
            if name[0] >= "0" and name[0] <="9":
                for c in name:
                    if not(c >="0" and c<="9"):
                        print(f"lexer error: invalid token {name} must be number or name")
                        exit()
        elif self.code[start] == "\"":
            while self.has_next() and self.code[self.cursor] != "\"":
                if self.code[self.cursor] == "\n":
                    print("lexer error: \" is expected to end string")
                    exit()
                elif not self.has_next():
                    print("lexer error: \" is expected to end string")
                    exit()
                self.cursor+=1
            if self.has_next(): #this is to catch quote if there is one
                self.cursor+=1
        self.cur_token.capture_token(self.code[start:self.cursor])
        s = token_class_to_str(self.cur_token.token_class)
        self.tree += f"<{s}> {self.cur_token.name} </{s}>\n"

    def lex_class_var_dec(self): # fix so it parses comma separated declarations
        self.tree+="<classVarDec>\n"
        self.lex_next_token() 
        if self.cur_token.token_type != Token_Type.FIELD and self.cur_token.token_type != Token_Type.STATIC:
            print("field or static expected brudder!! not " + self.cur_token.name)
            exit()
        self.lex_type()
        while True:
            self.lex_identifier()
            self.lex_next_token()
            if self.cur_token.token_type == Token_Type.SEMICOLON:
               break
            elif self.cur_token.token_type == Token_Type.COMMA:
               pass
            else:
               print("error in class var declaration")
               exit()
        self.tree+="</classVarDec>\n"

    
    def lex_class_def(self): 
        self.tree+="<class>\n"
        self.lex_expected_token(Token_Type.CLASS)
        self.lex_identifier()
        self.lex_expected_token(Token_Type.LEFT_CURLY)
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.STATIC or self.cur_token.token_type == Token_Type.FIELD:
                self.lex_class_var_dec()
            elif self.cur_token.token_type == Token_Type.FUNCTION or self.cur_token.token_type == Token_Type.METHOD or self.cur_token.token_type == Token_Type.CONSTRUCTOR:
                self.lex_subroutine_dec()
            elif self.cur_token.token_type == Token_Type.RIGHT_CURLY:
                self.lex_next_token()
                break
            else:
                print("error invalid class definition!!!!")
                exit()
        self.tree+="</class>\n"
        
    def peek_ahead(self,k):
        saved_tree_state = self.tree
        start = self.cursor
        i = 0
        while i < k:
            self.lex_next_token()
            i+=1
        self.cursor = start
        self.tree = saved_tree_state
        
    def lex_subroutine_dec(self): 
        self.tree+="<subroutineDec>\n"
        self.lex_next_token()
        if not(self.cur_token.token_type == Token_Type.FUNCTION or self.cur_token.token_type == Token_Type.METHOD or self.cur_token.token_type == Token_Type.CONSTRUCTOR):
            print("error must be a subroutine not " + token.name)
            exit()
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
        self.tree+="<statements>\n"
        while True:
            self.lex_statement()
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.RIGHT_CURLY:
                break
            elif self.cur_token.token_type == Token_Type.INVALID:
                print("} is expected g not " + token.name)
                exit()
        self.tree+="</statements>\n"
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
                print("error in var declaration ; is expected ")
                exit()
        self.tree+="</varDec>\n"

    def lex_type(self): 
        self.lex_next_token()
        if not(self.cur_token.token_type == Token_Type.INT or self.cur_token.token_type == Token_Type.CHAR or self.cur_token.token_type == Token_Type.BOOL or self.cur_token.token_type == Token_Type.IDENTIFIER):
            print("invalid type " + token.name)
            exit()

    #set of statement functions
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
            print("invalid statement!!!" + self.cur_token.name)
            exit()

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
        self.tree+="<statements>\n"
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.RIGHT_CURLY:
                break
            self.lex_statement()
        self.tree+="</statements>\n"
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
        self.tree+="<statements>\n"
        while True:
            self.peek_ahead(1)
            if self.cur_token.token_type == Token_Type.RIGHT_CURLY:
                break
            self.lex_statement()
        self.tree+="</statements>\n"
        self.lex_expected_token(Token_Type.RIGHT_CURLY)
        self.peek_ahead(1)
        if self.cur_token.token_type == Token_Type.ELSE:
            self.lex_expected_token(Token_Type.ELSE)
            self.lex_expected_token(Token_Type.LEFT_CURLY)
            self.tree+="<statements>\n"
            while True:
                self.peek_ahead(1)
                if self.cur_token.token_type == Token_Type.RIGHT_CURLY:
                    break
                self.lex_statement()
            self.tree+="</statements>\n"
            self.lex_expected_token(Token_Type.RIGHT_CURLY)
        self.tree+="</ifStatement>\n"

    def lex_let_statement(self):
        self.tree+="<letStatement>\n"
        self.lex_expected_token(Token_Type.LET)
        self.lex_identifier()
        self.lex_next_token()
        if self.cur_token.token_type == Token_Type.LEFT_BRACKET:
            self.lex_expression() 
            self.lex_expected_token(Token_Type.RIGHT_BRACKET)
            self.lex_expected_token(Token_Type.EQUALS)
        elif self.cur_token.token_type != Token_Type.EQUALS:
            print("equals expected for let statement")
            exit()
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
            print("error bad term " + self.cur_token.name)
            exit()
        self.tree+="</term>\n"

    def lex_subroutine_call(self):
        self.lex_identifier()
        self.lex_next_token()
        if self.cur_token.token_type == Token_Type.DOT:
            self.lex_identifier()
            self.lex_expected_token(Token_Type.LEFT_PAREN)
        elif self.cur_token.token_type != Token_Type.LEFT_PAREN:
                print("lexer error: ( is missing in subroutine call")
                exit()
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
            print("expected identifier for let statement")
            exit()

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
            print(f"lexer error: expected {tt}, got {self.cur_token.name} instead")
            print(self.tree)
            exit()
    
def is_alphanumeric(c):
    return (c >="0" and c<="9") or (c >="A" and c <="Z") or (c >="a" and c <="z") or c =="_"
