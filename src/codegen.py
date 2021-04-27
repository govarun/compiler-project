from reg_funcs import *
from helper_functions import *
from parser import symbol_table, local_vars, strings
class CodeGen:
    def gen_top_headers(self):
        print('extern printf')
        print("section .text")
        print("\tglobal main")

    def data_section(self):
        print("section\t.data")
        for vars in symbol_table[0].keys():
            if 'isFunc' not in symbol_table[0][vars].keys() and vars not in strings.keys():
                print("\t" + vars + "\tdd\t0")
        print("\tgetInt:\tdb\t\"%d\"\t")
        for name in strings.keys():
            print("\t" + name + ":\tdb\t" + strings[name] + ", 0")

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


    def param(self, quad):
        print("\tpush " + get_best_location(quad.src1))
        pass

    def function_call(self, quad):
        save_caller_status()
        print("\tcall " + quad.src1)
        if(len(quad.src2)):
            print("\tmov " + get_best_location(quad.src2) + ", eax")
        for var in local_vars[quad.src1]:
            symbols[var].address_desc_mem.pop()
        print("\tadd esp, " + str(4*len(func_arguments[quad.src1])))

    def alloc_stack(self,quad):
        '''
        Allocate stack space for function local variables
        '''
        print(quad.src1 + ":")
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
        
        print("\tmov esp, ebp")
        print("\tpop ebp")
        print("\tret")

    def generate_asm(self, quad):
        '''
        Function to generate final asm code
        '''
        if(quad.op == "func"):
            self.alloc_stack(quad)
        elif(quad.op == "param"):
            self.param(quad)
        elif(quad.op == "call"):
            self.function_call(quad)
        elif(quad.op.endswith("=")):
            self.assign(quad)
        elif(quad.op == "ret"):
            self.function_return(quad)

def runmain():
    codegen = CodeGen()
    codegen.gen_top_headers()
    for quad in instruction_array:
        codegen.generate_asm(quad)

    codegen.data_section()
