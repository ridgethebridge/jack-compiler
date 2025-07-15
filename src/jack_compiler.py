
from code_generator import *
generator = Code_Generator(input("enter the file "))
generator.compile_class()
generator.dump_vm("test.vm")
