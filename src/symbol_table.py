

class Table:
    def __init__(self):
        self.table = {}

    def define(self,name,t_type,kind,index):
        self.table[name] = (t_type,kind,index)
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
