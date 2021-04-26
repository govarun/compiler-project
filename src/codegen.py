from reg_funcs import *
from parser import symbol_table, local_vars
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
        #check where moved back into memory
        reg1 = get_register(quad)
        if(not reg1.startswith("[")):
            print("\tmov " + reg1 + ", " + get_best_location(quad.src1))
        reg2 = get_best_location(quad.src2)
        print("\tadd " + reg1 + ", " + reg2)
        upd_reg_desc(reg1,quad.dest)
        free_all_regs(quad)

def runmain():
    codegen = CodeGen()
    codegen.gen_top_headers()
    codegen.data_section()