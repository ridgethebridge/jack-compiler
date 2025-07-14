
from code_generator import *
generator = Code_Generator("../tests/compiler/Average/Main.jack")
generator.compile_class()
generator.dump_vm("test.vm")
