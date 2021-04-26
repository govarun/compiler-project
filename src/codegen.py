from reg_funcs import *
from helper_funcs import *
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
        reg1 = get_register(quad, compulsory = True)
        upd_reg_desc(reg1, quad.src1)
        print("\tmov " + reg1 + ", " + get_best_location(quad.src1))
        reg2 = get_best_location(quad.src2) 
        print("\tadd " + reg1 + ", " + reg2)
        upd_reg_desc(reg1,quad.dest)
        free_all_regs(quad)

    def assign(self, quad):
        if (quad.src2 is not None): # case for pointer
            pass 
        elif (is_number(quad.src1)): # case when src1 is an integral numeric
            best_location = get_best_location(quad.dest)
            if (check_location_type(best_location) == "register"):
                upd_reg_desc(best_location, quad.dest)
            print("\tmov " + best_location + ", " + int(quad.src1))
        else:
            best_location = get_best_location(quad.src1)
            if (check_type_location(best_location) in ["memory", "data"]):
                reg = get_register(quad.src1, compulsory = True)
                upd_reg_desc(reg, quad.src1)
                print("\tmov " + reg + ", " + best_location)

            best_location = get_best_location(quad.src1)
            if (check_type_location(best_location) in ["register"]):
                symbols[quad.dest].address_desc_reg.add(best_location)
                reg_desc[best_location].add(quad.dest)
                del_symbol_reg_exclude(quad.dest, [best_location])

            if (quad.instr_info['nextuse'][quad.src1] == None):
                del_symbol_reg_exclude(quad.src1)



def runmain():
    codegen = CodeGen()
    codegen.gen_top_headers()
    codegen.data_section()