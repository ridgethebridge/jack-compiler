
'''
recap:
initially classes and functions will not be in a table
this means that functions which don't exist and classes which don't exist will compile fine, fix soon
--------------------------------------
TODO:
7/13/2025
add type checking for return method so correct type gets returned, also 0 should be reutrned for void functions
function calls need arity check, and type checking for parameters, also function identifiers should be realized prior to use so check for that
--------------------------------------
'''

from jack_lexer import *
from symbol_table import *
from token import Token_Class as tc
from token import Token_Type as tt

#kinds for identifiers and segments
LOCAL = "local"
ARGUMENT = "argument"
STATIC = "static"
CLASS = "class"
SUB = "subroutine"
FIELD = "field"
POINTER = "pointer"
CONSTANT = "constant"
TEMP = "temp"
THIS="this"
THAT="that"
UNDEFINED = None


#indices for table
TYPE_INDEX = 0
KIND_INDEX = 1
INDEX_INDEX = 2

operations = {"+":"add","-":"sub","*":"call Math.multiply 2","/":"call Math.divide 2","~":"not",
              "=":"eq","|":"or","&":"and",">":"gt",
              "<":"lt"}

class Code_Generator:

    def __init__(self,file):
         self.lexer = Jack_Lexer(file)
         self.output = ""
         self.if_label_num = 0
         self.while_label_num=0
         self.g_table = Table()
         self.l_table = Table()
         self.c_table = Table()
         self.kind_table = {"field":0,"static":0,"local":0,"argument":0}

    def write_push(self,segment,index):
        self.output+=f"push {segment} {index}\n"

    def write_pop(self,segment,index):
        self.output+=f"pop {segment} {index}\n"

    def write_arithmetic(self,operation):
        self.output+=f"{operations[operation]}\n"

    def write_label(self,is_if):
        if is_if:
            self.output+=f"label I_L{self.if_label_num}\n"
            self.if_label_num+=1
        else:
            self.output+=f"label W_L{self.while_label_num}\n"
            self.while_label_num+=1

    def write_goto(self,label):
        self.output+=f"goto {label}\n"

    def write_ifgoto(self,label):
        self.output+=f"if-goto {label}\n"

    def write_call(self,name,num_args):
        self.output+=f"call {name} {num_args}\n"

    def write_function(self,name,num_locals):
        self.output+=f"function {self.lexer.cur_file.split(".")[0]}.{name} {num_locals}\n"

    def write_string(self,string):
        self.write_push(CONSTANT,len(string))
        self.write_call("String.new",1)
        for c in string:
            self.write_push(CONSTANT,ord(c))
            self.write_call("String.appendChar",2)


    def get_segment(self,kind):
        if kind == "field":
            return "this"
        return kind

    def compile_identifier(self,name):
        var = self.use_identifier()
        self.write_push(self.get_segment(var[KIND_INDEX]),var[INDEX_INDEX])

    #for assignments and maybe function calls
    def use_identifier(self):
        self.lexer.lex_identifier()
        t = self.lexer.cur_token
        is_array = False
        if t.name in self.l_table:
            var = self.l_table.table[t.name]
        elif t.name in self.g_table:
            var = self.g_table.table[t.name]
        elif t.name in self.c_table:
            var = self.c_table.table[t.name]
        else:
            print(f"undefined identifier {t.name} {self.lexer.cur_line}:{self.lexer.line_pos}")
            exit()
        self.lexer.peek_ahead(1)
        if self.lexer.cur_token.token_type == tt.LEFT_BRACKET:
            self.write_push(self.get_segment(var[KIND_INDEX]),var[INDEX_INDEX])
            is_array = True
            self.lexer.lex_expected_tokens([tt.LEFT_BRACKET])
            self.compile_expression() 
            self.lexer.lex_expected_tokens([tt.RIGHT_BRACKET])
            self.write_arithmetic("+")
            self.write_pop(POINTER,1)
        return var, is_array

    def compile_class(self):
        self.lexer.lex_expected_tokens([tt.CLASS])
        self.lexer.lex_identifier()
        self.c_table.define(self.lexer.cur_token.name,CLASS,CLASS,0)
        self.lexer.lex_expected_tokens([tt.LEFT_CURLY])
        t = self.lexer.peek_ahead(1)
        while t.token_type == tt.STATIC or t.token_type == tt.FIELD:
            self.compile_class_var_dec()
            t = self.lexer.peek_ahead(1)
        t = self.lexer.peek_ahead(1)
        while t.token_type == tt.METHOD or t.token_type == tt.CONSTRUCTOR or t.token_type == tt.FUNCTION:
            self.compile_subroutine_dec()
            t = self.lexer.peek_ahead(1)
        self.lexer.lex_expected_tokens([tt.RIGHT_CURLY])


    #subroutine functions
    def compile_subroutine_dec(self):
        self.l_table.start_routine()#resets local table
        self.kind_table["local"] = 0
        self.kind_table["argument"] = 0 #resets count each func declaration
        t_kind = self.lexer.lex_expected_tokens([tt.FUNCTION,tt.METHOD,tt.CONSTRUCTOR])
        t_type = self.lexer.peek_ahead(1)
        if t_type.token_type == tt.VOID:
            self.lexer.lex_expected_tokens([tt.VOID])
        else:
            self.lexer.lex_type()
        t_name =self.lexer.lex_identifier()
        self.lexer.lex_expected_tokens([tt.LEFT_PAREN])
        self.compile_parameter_list() 
        self.lexer.lex_expected_tokens([tt.RIGHT_PAREN])
        self.compile_subroutine_body(t_name.name,t_kind) 

    def compile_parameter_list(self):
        self.lexer.peek_ahead(1)
        if self.lexer.cur_token.token_type != tt.RIGHT_PAREN:
            t_type=self.lexer.lex_type()
            t_name =self.lexer.lex_identifier()
            self.l_table.define(t_name.name,t_type.name,ARGUMENT,self.kind_table[ARGUMENT])
            self.kind_table[ARGUMENT]+=1
            self.lexer.peek_ahead(1)
            while self.lexer.cur_token.token_type == tt.COMMA:
                self.lexer.lex_expected_tokens([tt.COMMA]) 
                t_type=self.lexer.lex_type()
                t_name =self.lexer.lex_identifier()
                self.l_table.define(t_name.name,t_type.name,ARGUMENT,self.kind_table[ARGUMENT])
                self.kind_table[ARGUMENT]+=1
                self.lexer.peek_ahead(1) 

    def compile_subroutine_body(self,func_name,kind_token):
        self.lexer.lex_expected_tokens([tt.LEFT_CURLY])
        while True:
            self.lexer.peek_ahead(1)
            if self.lexer.cur_token.token_type == tt.VAR:
                self.compile_var_dec()
            else:
                break
        #now time to write function label
        self.write_function(func_name,self.kind_table[LOCAL])
        #checks for method and constructor
        if kind_token.token_type == tt.METHOD:
            self.write_push(ARGUMENT,0)
            self.write_pop(POINTER,0)
        elif kind_token.token_type == tt.CONSTRUCTOR:
            self.write_push(CONSTANT,self.kind_table[FIELD])
            self.write_call("Memory.alloc",1)
            self.write_pop(POINTER,0)
        self.compile_multiple_statements()
        self.lexer.lex_expected_tokens([tt.RIGHT_CURLY]) 

    def compile_var_dec(self):
        self.lexer.lex_expected_tokens([tt.VAR])
        t_type = self.lexer.lex_type()
        while True:
            t_name = self.lexer.lex_identifier()
            self.l_table.define(t_name.name,t_type.name,LOCAL,self.kind_table[LOCAL])
            self.kind_table[LOCAL]+=1
            self.lexer.lex_expected_tokens([tt.COMMA,tt.SEMICOLON])
            if self.lexer.cur_token.token_type != tt.COMMA:
                break

    def compile_class_var_dec(self):
        t = self.lexer.lex_expected_tokens((tt.FIELD,tt.STATIC))
        t_type = self.lexer.lex_type()
        while True:
            t_name = self.lexer.lex_identifier()
            self.g_table.define(t_name.name,t_type.name,t.name,self.kind_table[t.name])
            self.kind_table[t.name]+=1 #updates either field or static
            self.lexer.lex_expected_tokens([tt.COMMA,tt.SEMICOLON])
            if self.lexer.cur_token.token_type != tt.COMMA:
                break

    #set of expression functions
    #@fix
    #work on whats written into vm code
    #fix string and this handling
    #add support fo unary operators
    #add support fo array indexing
    #check to make sure identifiers exist in table
    def compile_term(self):
        self.lexer.peek_ahead(1)
        if self.lexer.cur_token.token_type == tt.INT_CONSTANT:
           self.lexer.lex_next_token()
           self.write_push("constant",self.lexer.cur_token.name)
        elif self.lexer.cur_token.token_type == tt.STRING_CONSTANT: 
           self.lexer.lex_next_token()
           self.write_string(self.lexer.cur_token.name)
        elif self.lexer.cur_token.token_type == tt.TRUE: 
            self.lexer.lex_next_token()
            self.write_push("constant","1") #@fix
        elif self.lexer.cur_token.token_type == tt.FALSE: 
            self.lexer.lex_next_token()
            self.write_push("constant","0")
        elif self.lexer.cur_token.token_type == tt.NULL: 
            self.lexer.lex_next_token()
            self.write_push("constant","0")
        elif self.lexer.cur_token.token_type == tt.THIS: 
            self.lexer.lex_next_token()
            self.write_push("pointer","0")
        elif self.lexer.cur_token.token_type == tt.LEFT_PAREN:
            self.lexer.lex_expected_tokens([tt.LEFT_PAREN])
            self.compile_expression()
            self.lexer.lex_expected_tokens([tt.RIGHT_PAREN])
        elif self.lexer.cur_token.token_type == tt.MINUS or self.lexer.cur_token.token_type == tt.TILDE:
            t = self.lexer.lex_next_token() # maybe make a function for it?
            self.compile_term()
            self.write_arithmetic(t.name)
        elif self.lexer.cur_token.token_type == tt.IDENTIFIER:
            self.lexer.peek_ahead(2)
            if self.lexer.cur_token.token_type == tt.LEFT_BRACKET:
                var,_ = self.use_identifier()
                self.write_push("that",0)
            elif self.lexer.cur_token.token_type == tt.LEFT_PAREN or self.lexer.cur_token.token_type == tt.DOT:
                self.compile_subroutine_call() 
            else: 
                var,_ = self.use_identifier()
                self.write_push(self.get_segment(var[KIND_INDEX]),var[INDEX_INDEX])
        else:
            self.lexer.report_error(f"syntax error: invalid term for expression, identifier, constant or expression expected, not {self.lexer.cur_token.name}\n")
            self.lexer.lex_next_token() 

    def compile_expression(self):
        self.compile_term() 
        while True:
            self.lexer.peek_ahead(1)
            if self.lexer.cur_token.token_class == Token_Class.OPERATOR:
                t = self.lexer.lex_next_token() #check for proper operator
                self.compile_term()
                self.write_arithmetic(t.name)
            else:
                break
    #TODO translate function calls, ensure types and number of parameters matches definition
    # and also make sure function exists
    def compile_subroutine_call(self):
        num_args = 0
        first_name = self.lexer.lex_identifier()
        last_name = None
        self.lexer.peek_ahead(1)
        if self.lexer.cur_token.token_type == tt.DOT:
            self.lexer.lex_expected_tokens(tuple([tt.DOT]))
            last_name = self.lexer.lex_identifier()
        #to see if it is an object
        var_type = self.token_to_identifier(first_name)
        call_written = None
        if var_type != None:
            self.write_push(self.get_segment(var_type[KIND_INDEX]),var_type[INDEX_INDEX])
            num_args+=1
            call_written = f"{var_type[TYPE_INDEX]}.{last_name.name}"
        elif last_name == None:
            self.write_push(ARGUMENT,0)
            num_args+=1
            class_name = self.lexer.cur_file.replace(".jack","")
            call_written = f"{class_name}.{first_name.name}"
        else:
            class_name = self.lexer.cur_file.replace(".jack","")
            call_written = f"{first_name.name}.{last_name.name}"
        self.lexer.lex_expected_tokens([tt.LEFT_PAREN])
        self.lexer.peek_ahead(1)
        if self.lexer.cur_token.token_type == tt.RIGHT_PAREN:
            self.lexer.lex_expected_tokens((tt.RIGHT_PAREN,))
            self.write_call(call_written,num_args)
            return
        while self.lexer.cur_token.token_type != tt.RIGHT_PAREN:
            num_args+=1
            self.compile_expression()
            self.lexer.lex_expected_tokens((tt.COMMA,tt.RIGHT_PAREN))
        self.write_call(call_written,num_args)

    #set of statment functions
    def compile_multiple_statements(self):
        while True:
            self.lexer.peek_ahead(1)
            if self.lexer.cur_token.token_type == tt.RIGHT_CURLY:
                break
            self.compile_statement()

    #all statements are assumed to have been read already
    def compile_let_statement(self):
        var,is_array = self.use_identifier()
        self.lexer.lex_expected_tokens([tt.EQUALS])
        self.compile_expression() 
        self.lexer.lex_expected_tokens([tt.SEMICOLON])
        if is_array:
            self.write_pop(THAT,0)
        else:
            self.write_pop(self.get_segment(var[KIND_INDEX]),var[INDEX_INDEX])

    def compile_if_statement(self):
        self.lexer.lex_expected_tokens((tt.LEFT_PAREN,))
        self.compile_expression()
        self.lexer.lex_expected_tokens((tt.RIGHT_PAREN,))
        self.lexer.lex_expected_tokens((tt.LEFT_CURLY,))
        self.lexer.peek_ahead(2)
        self.write_ifgoto(f"I_L{self.if_label_num}")
        self.write_goto(f"I_L{self.if_label_num+1}")
        self.write_label(True)
        self.compile_multiple_statements()
        self.lexer.lex_expected_tokens((tt.RIGHT_CURLY,))
        self.write_label(True)
        self.lexer.peek_ahead(1)
        if self.lexer.cur_token.token_type == tt.ELSE:
            self.lexer.lex_expected_tokens((tt.ELSE,))
            self.lexer.lex_expected_tokens((tt.LEFT_CURLY,))
            self.compile_multiple_statements()
            self.lexer.lex_expected_tokens((tt.RIGHT_CURLY,))

    def compile_while_statement(self):
        self.lexer.lex_expected_tokens([tt.LEFT_PAREN])
        self.write_label(False)#L0
        self.compile_expression()
        self.lexer.lex_expected_tokens([tt.RIGHT_PAREN])
        self.lexer.lex_expected_tokens([tt.LEFT_CURLY])
        self.write_ifgoto(f"W_L{self.while_label_num}") #L1
        self.write_goto(f"W_L{self.while_label_num+1}")#L2
        self.write_label(False)#L1
        self.compile_multiple_statements()
        self.write_goto(f"W_L{self.while_label_num-2}") #L0
        self.lexer.lex_expected_tokens([tt.RIGHT_CURLY])
        self.write_label(False)#L2

    def compile_do_statement(self):
        self.compile_subroutine_call()
        self.lexer.lex_expected_tokens([tt.SEMICOLON])

    
    def compile_return_statement(self):
        self.lexer.peek_ahead(1)
        if self.lexer.cur_token.token_type != tt.SEMICOLON:
            self.compile_expression()
        self.lexer.lex_expected_tokens([tt.SEMICOLON])
        self.output+="return\n"

#table for statement functions
    statement_maps = {
    tt.LET: compile_let_statement,
    tt.IF:compile_if_statement,
    tt.WHILE:compile_while_statement,
     tt.DO:compile_do_statement,
    tt.RETURN:compile_return_statement
    }

    def compile_statement(self):
        self.lexer.lex_expected_tokens([tt.DO,tt.LET,tt.WHILE,tt.IF,tt.RETURN])
        if not(self.lexer.cur_token.token_type in self.statement_maps):
            return
        self.statement_maps[self.lexer.cur_token.token_type](self)

    def dump_vm(self,file_name):
        with open(file_name,"w") as f:
            f.write(self.output)

    def token_to_identifier(self,token):
        if token.name in self.l_table:
            return self.l_table.table[token.name]
        elif token.name in self.g_table:
            return self.g_table.table[token.name]
        return None
