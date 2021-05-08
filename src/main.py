import parser
import sys
import lexer
import codegen
import helper_functions
from lexer import syn_error_count
s = str(sys.argv)
if(len(sys.argv) <= 1):
	print("Incorrect Usage")
	print('Usage: python3 main.py ([--help] | file name [--lexer])')
	exit()
if(sys.argv[1] == "--help"):
	print('Usage: python3 main.py ([--help] | file name [--lexer])')
	print('Options-')
	print('--help : \t Small tutorial on how to use the compiler')
	print('--lexer : \t Use only lexer (no parsing)\n')
	print('Dependencies:')
	print('This compiler makes use of the following python3 packages:')
	print('1. ply')
	print('2. tabulate')
	print('3. pydot\n')
	print('To install these dependencies, simply run "pip install -r requirements.txt"(without quotes) from the root of the repo')
	exit()

if(len(sys.argv) >= 3 and sys.argv[2] == "--lexer"):
	file = open(sys.argv[1])
	code = file.read()
	if __name__ == '__main__':
		lexer.runmain(code)
	exit()
	# for i in range(len(sys.argv)-1):
	# file = open(sys.argv[i+1])
	# code = file.read()
	# # print(code)
	# print(sys.argv[i+1])
	# if __name__ == '__main__':
	# 	lexer.runmain(code)	


file = open(sys.argv[1])
code = file.read()
if __name__ == '__main__':
	parser.runmain(code)
	helper_functions.runmain()
	global syn_error_count
	print('main.py : syn_error_count = ', syn_error_count)
	if syn_error_count == 0:
		codegen.runmain()
	else:
		print('main.py : number of errors is non-zero')