import parser
import sys
s = str(sys.argv)
if(len(sys.argv) <= 1):
	print("Incorrect Usage")
	print("Correct Usage: python3 main.py [--help] | [file names seperated by space]")
	exit()
if(sys.argv[1] == "--help"):
	print('Usage: python3 main.py [--help | file names seperated by space]')
	print('Options-')
	print('--help : \t Small tutorial on how to use the compiler\n')
	print('Dependencies:')
	print('This compiler makes use of the following python3 packages:')
	print('1. ply')
	print('2. tabulate\n')
	print('To install these dependencies, simply run "pip install -r requirements.txt"(without quotes) from the root of the repo')
	exit()
for i in range(len(sys.argv)-1):
	file = open(sys.argv[i+1])
	code = file.read()
	# print(code)
	print(sys.argv[i+1])
	if __name__ == '__main__':
		parser.runmain(code)
