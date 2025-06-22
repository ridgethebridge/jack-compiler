
from jack_lexer import *





operations = {"+":"add","-":"sub","~":"not",
              "=":"eq","|":"or","&":"and",">":"gt",
              "<":"lt"}

class Code_Generator:

    def __init__(self,file):
         self.lexer = Jack_Lexer(file)
         self.output = ""
         self.label_num = 0
         self.g_table = Table()
         self.l_table = Table()
         self.c_table = Table()

    def write_push(self,segment,index):
        sel.output+=f"push {segment} {index}\n"

    def write_pop(self,segment,index):
        sel.output+=f"pop {segment} {index}\n"

    def write_arithmetic(self,operation):
        self.output+=f"{operations[operation]}\n"

    def write_label(self,name):
        self.output+=f"label L{self.label_num}\n"
        self.label_num+=1

    def write_goto(self,label):
        self.output+="goto {label}\n"

    def write_ifgoto(self,label):
        self.output+="goto {label}\n"

    def write_call(self,name,num_args):
        self.output+=f"call {name} {num_args}\n"

    def write_function(self,name,num_locals):
        self.output+=f"function {name} {num_locals}\n"





