from parser import symbol_table
class CodeGen:
    def gen_top_headers(self):
        print("section .text")
        print("\tglobal main")

    def data_section(self):
        print('extern printf')
        print("section\t.data\n")
        for vars in symbol_table[0].keys():
            print(vars + "\tdd\t0")

    def add(self,quad):
        reg1, flag = 

def runmain():
    codegen = CodeGen()
    codegen.gen_top_headers()
    codegen.data_section()