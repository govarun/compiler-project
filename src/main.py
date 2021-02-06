import lexer
import sys
s = str(sys.argv)
if(len(sys.argv) <= 1):
	print("No file specified")
	exit()
# print(s[13:-2])
file = open(s[13:-2]) # hardcoded since "main.py" is a fixed name
code = file.read()
# print(code)
# lexer = lexer.lex()
# lexer.inputcode)
if __name__ == '__main__':
	lexer.runmain(code)
