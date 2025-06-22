
#kinds for identifiers
LOCAL = "local"
ARG = "argument"
STATIC = "static"
CLASS = "class"
SUB = "subroutine"
FIELD = "field"
UNDEFINED = None

class Table:
    def __init__(self):
        self.table = {}
        self.index = 0
    def define(self,name,t_type,kind):
        self.table[name] = (t_type,kind,self.index)
        self.index+=1
    def var_count(self,kind):
        count = 0
        for k, v in self.table:
            if v[1] == kind:
                count+=1
        return count
    def kind(self,name):
        return self.table[name][1]
    def index_of(self,name):
        return self.table[name][2]
    def type_of(self,name):
        return self.table[name][0]
    def start_routine(self):
        del(self)
        self = Table()

    def __contains__(self,item):
        return item in self.table
