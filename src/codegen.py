from reg_funcs import *
from helper_functions import *
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
        best_location = get_best_location(quad.src1)
        upd_reg_desc(reg1, quad.src1)
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)
        reg2 = get_best_location(quad.src2) 
        print("\tadd " + reg1 + ", " + reg2)
        upd_reg_desc(reg1,quad.dest)
        free_all_regs(quad)

    def sub(self, quad):
        #check where moved back into memory
        reg1 = get_register(quad, compulsory=True)
        best_location = get_best_location(quad.src1)
        upd_reg_desc(reg1, quad.src1)
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)
        reg2 = get_best_location(quad.src2)
        print("\tsub " + reg1 + ", " + reg2)
        upd_reg_desc(reg1, quad.dest)
        free_all_regs(quad)


    def assign(self, quad):
        if (quad.src2 is not None): # case for pointer
            pass 
        elif (is_number(quad.src1)): # case when src1 is an integral numeric
            best_location = get_best_location(quad.dest)
            if (check_type_location(best_location) == "register"):
                upd_reg_desc(best_location, quad.dest)
            print("\tmov " + best_location + ", " + int(quad.src1))
        else:
            best_location = get_best_location(quad.src1)
            if (check_type_location(best_location) in ["memory", "data"]):
                reg = get_register(quad, compulsory = True)
                upd_reg_desc(reg, quad.src1)
                print("\tmov " + reg + ", " + best_location)
                best_location = reg

            symbols[quad.dest].address_desc_reg.add(best_location)
            reg_desc[best_location].add(quad.dest)
            del_symbol_reg_exclude(quad.dest, [best_location])

            if (quad.instr_info['nextuse'][quad.src1] == None):
                del_symbol_reg_exclude(quad.src1)


    def param(self, quad):
        print("\tpush " + get_best_location(quad.src1))
        pass

    def function_call(self, quad):
        save_caller_status()
        print("\tcall " + quad.src1)
        print("\tmov " + get_best_location(quad.src2) + ", eax")
        print("\tadd esp, " + str(4*len(func_arguments[quad.src1])))

    def alloc_stack(self,quad):
        '''
        Allocate stack space for function local variables
        '''
        print(quad.src1)
        counter = 0
        for var in local_vars[quad.src1]:
            if var not in func_arguments[quad.src1]:
                counter += 1
                symbols[var].address_desc_mem.append(-4*counter) #why is the first loc variable at ebp -4 and not at ebp

        print("\tpush ebp")
        print("\tmov ebp, esp")
        print("\tsub esp, " + str(4*counter))

        counter = 0
        for var in func_arguments[quad.src1]:
            symbols[var].address_desc_reg.append(4*counter + 8)
            counter += 1

    def function_return(self, quad):
        if(quad.src1):
            location = get_best_location(quad.src1)
            save_reg_to_mem("eax")
            if(location is not "eax"):
                print("\tmov eax, " + str(location))

        for var in local_vars[quad.src1]:
            symbols[var].address_desc_mem.pop()
        
        print("\tmov esp, ebp")
        print("\tpop ebp")
        print("\tret")

def runmain():
    codegen = CodeGen()
    codegen.gen_top_headers()
    codegen.data_section()
