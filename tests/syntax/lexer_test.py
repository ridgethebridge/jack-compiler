

import sys
import os
import subprocess
sys.path.insert(0,"/users/ridge/coding/hack-compiler/src")
from xml_generator import *
from jack_lexer import *
def main():
   folder_list = os.listdir(".")
   i = 0
   while i < len(folder_list):
       if not os.path.isdir(folder_list[i]):
           del(folder_list[i])
       else:
           i+=1
   
   for folder in folder_list:
       file_list = os.listdir(folder)
       file_list = [f for f in file_list if ".jack" in f] # maybe change to look for .jack at end
       for file in file_list:
           lexer = Jack_Lexer(f"{folder}/{file}")
           xml_result = compile_class(lexer)
           xml_name = lexer.cur_file.replace(".jack",".xml").split("/")[1]
           dump_xml_to_file(xml_result,xml_name)
           process_result = subprocess.run("comparer\\textcomparer.bat " f"{xml_name} {folder}\\{xml_name}",capture_output=True,text=True).stdout
           if not process_result == "Comparison ended successfully\n":
               print(f"{xml_name} is incorrectly lexed")
               print(lexer.error_log)
               exit()
   print("all files are good")
   subprocess.run("del *.xml",shell=True)
main()
