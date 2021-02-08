import lexer
import sys
s = str(sys.argv)
if(len(sys.argv) <= 1):
	print("No file specified")
	exit()
# print(sys.argv[1])

for i in range(len(sys.argv)-1):
	file = open(sys.argv[i+1])
	code = file.read()
	# print(code)
	print(sys.argv[i+1])
	if __name__ == '__main__':
		lexer.runmain(code)
