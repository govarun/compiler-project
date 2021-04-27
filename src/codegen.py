from reg_funcs import *
from helper_functions import *
from parser import symbol_table, local_vars, strings
import sys

def dprint(str):
    '''
    Function for debugging
    '''
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    print(str)
    sys.stdout = open('out.asm', 'a')


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

    def bin_operations(self, quad, op):
        #check where moved back into memory
        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True)
        save_reg_to_mem(reg1)
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)
        reg2 = get_best_location(quad.src2)
        print("\t" + op + ' ' + reg1 + ", " + reg2)
        upd_reg_desc(reg1, quad.dest)
        for sym in reg_desc[reg1]:
            dprint(reg1 + ", " + sym)
        free_all_regs(quad)

    def add(self,quad):
        self.bin_operations(quad, 'add')

    def sub(self, quad):
        self.bin_operations(quad, 'sub')

    def mul(self, quad):
        self.bin_operations(quad, 'imul')
    
    def div(self, quad):
        best_location = get_best_location(quad.src1)
        save_reg_to_mem('eax')
        save_reg_to_mem('edx')
        if best_location != 'eax':
            print("\tmov " + 'eax' + ", " + best_location)
        reg = get_register(quad, exclude_reg=['eax','edx'])
        best_location = get_best_location(quad.src2)
        upd_reg_desc(reg, quad.src2)
        if best_location != reg:
            print("\tmov " + reg + ", " + best_location)
        print("\tcdq")
        print('\tidiv ' + reg)
        upd_reg_desc('eax', quad.dest)

        for sym in reg_desc['eax']:
            dprint('eax' + ", " + sym)

        free_all_regs(quad)

    def mod(self, quad):
        best_location = get_best_location(quad.src1)
        save_reg_to_mem('eax')
        save_reg_to_mem('edx')
        if best_location != 'eax':
            print("\tmov " + 'eax' + ", " + best_location)
        reg = get_register(quad, exclude_reg=['eax', 'edx'])
        best_location = get_best_location(quad.src2)
        upd_reg_desc(reg, quad.src2)
        if best_location != reg:
            print("\tmov " + reg + ", " + best_location)
        print("\tcdq")
        print('\tidiv ' + reg)
        upd_reg_desc('edx', quad.dest)

        for sym in reg_desc['edx']:
            dprint('edx' + ", " + sym)

        free_all_regs(quad)
    
    def lshift(self, quad):
        pass

    def assign(self, quad):
        if (quad.src2 is not None): # case for pointer
            pass 
        elif (is_number(quad.src1)): # case when src1 is an integral numeric
            best_location = get_best_location(quad.dest)
            if (check_type_location(best_location) == "register"):
                upd_reg_desc(best_location, quad.dest)
            print("\tmov " + best_location + ", " + quad.src1)
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
        print("\tpush " + str(get_best_location(quad.src1)))
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
            symbols[var].address_desc_mem.append(4*counter + 8)
            counter += 1

    def function_return(self, quad):
        if(quad.src1):
            location = get_best_location(quad.src1)
            save_reg_to_mem("eax")
            if(location != "eax"):
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
        elif(quad.op.endswith("+")):
            self.add(quad)
        elif(quad.op.endswith("-")):
            self.sub(quad)
        elif(quad.op.endswith("*")):
            self.mul(quad)
        elif(quad.op.endswith("/")):
            self.div(quad)
        elif(quad.op.endswith("%")):
            self.mod(quad)

def runmain():
    sys.stdout = open('out.asm', 'w')
    codegen = CodeGen()
    codegen.gen_top_headers()
    for quad in instruction_array:
        codegen.generate_asm(quad)
    codegen.data_section()
    sys.stdout.close()
