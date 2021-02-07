import lexer
import sys
s = str(sys.argv)
if(len(sys.argv) <= 1):
	print("No file specified")
	exit()
# print(sys.argv[1])

file = open(sys.argv[1])
code = file.read()
# print(code)

if __name__ == '__main__':
	lexer.runmain(code)
