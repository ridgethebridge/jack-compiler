
from token import *
from symbol_table import *
class Jack_Lexer:

    '''
    def new_identifier_info(self,i_type,kind,defined):
        self.tree+="<identifer-block>\n"
        self.lex_identifier()
        table = None
        if kind == FIELD or kind == FIELD:
            table = self.g_table
        else:
            table = self.l_table
        self.tree+=f"<type> {i_type} </type>\n"
        self.tree+=f"<kind> {kind} </kind>\n"
        self.tree+=f"<defined> {defined} </defined>\n"
        self.tree+="</identifer-block>\n"
        table.define(self.cur_token.name,i_type,kind)
        '''
    '''
    def used_identifier_info(self):
        self.tree+="<identifer-block>\n"
        self.lex_identifier()
        name = self.cur_token.name
        table = None
        if name in self.l_table:
            table = self.l_table.table
        elif name in self.g_table:
            table = self.g_table.table
        else:
            table = {name: ("undefined","undefined",-1)}
        self.tree+=f"<type> {table[name][0]} </type>\n"
        self.tree+=f"<kind> {table[name][1]} </kind>\n"
        self.tree+=f"<defined> {False} </defined>\n"
        self.tree+="</identifer-block>\n"
    '''

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
        
    def lex_identifier(self):
        self.lex_next_token()
        if self.cur_token.token_type != Token_Type.IDENTIFIER:
            self.error_log+=f"syntax error: identifier is expected not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"

    def has_next(self):
        return len(self.code) - self.cursor > 0


    def lex_expected_token(self,tt):
        self.peek_ahead(1)
        if self.cur_token.token_type != tt:
            self.error_log+=f"syntax error:  expected {tt} not {self.cur_token.name}\n"
            self.error_log+=f"{self.cur_file}: line {self.cur_line}:{self.line_pos}\n"
            return 
        self.lex_next_token()
    
