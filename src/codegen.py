from reg_funcs import *
from helper_functions import *
from parser import symbol_table, local_vars, strings, get_label, label_cnt
import sys
diction = {"&&" : "and", "||" : "or", "|" : "or", "&" : "and", "^" : "xor"}
param_count = 0
relational_op_list = ["<",">","<=",">=","==","!="] 

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
        print('extern scanf')
        print("section .text")
        print("\tglobal main")

    def data_section(self):
        print("section\t.data")
        for vars in local_vars['global']:
            if vars not in strings.keys():
                print("\t" + vars + "\tdd\t0")
        # print("\tgetInt:\tdb\t\"%d\"\t")
        for name in strings.keys():
            temp_string = (strings[name])[1:-1]
            print("\t" + name + ":\tdb\t`" + temp_string + "`, 0")

    def bin_operations(self, quad, op):
        #check where moved back into memory
        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True)
        save_reg_to_mem(reg1)
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)
        reg2 = get_best_location(quad.src2)
        print("\t" + op + ' ' + reg1 + ", " + reg2)
        free_all_regs(quad)
        upd_reg_desc(reg1, quad.dest)

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


        free_all_regs(quad)
    
    def increment(self, quad):
        best_location = get_best_location(quad.src1)
        if check_type_location(best_location) == "register":
            upd_reg_desc(best_location, quad.src1)
        print("\tinc " + best_location)

    def decrement(self, quad):
        best_location = get_best_location(quad.src1)
        if check_type_location(best_location) == "register":
            upd_reg_desc(best_location,quad.src1)
        print("\tdec " + best_location)

    def bitwisenot(self, quad):
        best_location = get_best_location(quad.dest)
        if check_type_location(best_location) == "register":
            upd_reg_desc(best_location, quad.dest)
        print("\tnot " + best_location)

    def uminus(self, quad):
        best_location = get_best_location(quad.dest)
        if check_type_location(best_location) == "register":
            upd_reg_desc(best_location, quad.dest)
        print("\tneg " + best_location)


    def lshift(self, quad):
        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True)
        upd_reg_desc(reg1, quad.dest)
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)
        
        best_location = get_best_location(quad.src2)
        if check_type_location(best_location) == "number":
            print("\tshl " + reg1 +  ', ' + best_location)
        else:
            if best_location != "ecx":
                upd_reg_desc("ecx",quad.src2)
                print("\tmov " + "ecx" + ", " + best_location)
            print("\tshl " + reg1 + ", cl")
        free_all_regs(quad)

    def rshift(self, quad):
        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True)
        upd_reg_desc(reg1, quad.dest)
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)

        best_location = get_best_location(quad.src2)
        if check_type_location(best_location) == "number":
            print("\tshr " + reg1 + ', ' + best_location)
        else:
            if best_location != "ecx":
                upd_reg_desc("ecx", quad.src2)
                print("\tmov " + "ecx" + ", " + best_location)
            print("\tshr " + reg1 + ", cl")
        free_all_regs(quad)
    
    def relational_op(self,quad):
        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True)
        save_reg_to_mem(reg1)
        op = quad.op.split("_")[-1]
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)
        reg2 = get_best_location(quad.src2)
        print("\t" + "cmp" + ' ' + reg1 + ", " + reg2)
        lbl = get_label()
        if(op == "<"):
            print("\tjl " + lbl)
        elif(op == ">"):
            print("\tjg " + lbl)
        elif(op == "=="):
            print("\tje " + lbl)
        elif(op == "!="):
            print("\tjne " + lbl)
        elif(op == "<="):
            print("\tjle " + lbl)
        elif(op == ">="):
            print("\tjge " + lbl)
        print("\tmov " + reg1 + ", 0")
        lbl2 = get_label()
        print("\tjmp " + lbl2)
        print(lbl + ":") 
        print("\tmov " + reg1 + ", 1")
        print(lbl2 + ":")
        upd_reg_desc(reg1, quad.dest)
        free_all_regs(quad)

    def assign(self, quad):
        if (quad.src2 is not None): # case for pointer
            pass 
        elif (is_number(quad.src1)): # case when src1 is an integral numeric
            best_location = get_best_location(quad.dest)
            if (check_type_location(best_location) == "register"):
                upd_reg_desc(best_location, quad.dest)
            print("\tmov " + best_location + ", " + quad.src1)
        else:
            #y_1 = t_1(eax)
            best_location = get_best_location(quad.src1)
            dprint(quad.src1 + " " + best_location + " " + quad.dest)
            if (check_type_location(best_location) in ["memory", "data", "number"]):
                reg = get_register(quad, compulsory = True)
                upd_reg_desc(reg, quad.src1)
                print("\tmov " + reg + ", " + best_location)
                best_location = reg

            symbols[quad.dest].address_desc_reg.add(best_location)
            reg_desc[best_location].add(quad.dest)
            del_symbol_reg_exclude(quad.dest, [best_location])

            # if (quad.instr_info['nextuse'][quad.src1] == None):
            #     del_symbol_reg_exclude(quad.src1)


    def param(self, quad):
        global param_count
        param_count += 1
        print("\tpush " + str(get_best_location(quad.src1)))

    def function_call(self, quad):
        global param_count
        save_caller_status()
        print("\tcall " + quad.src1)
        if(len(quad.src2)):
            print("\tmov " + get_best_location(quad.src2) + ", eax")
        print("\tadd esp, " + str(4*param_count))
        param_count = 0

    def funcEnd(self, quad):
        for var in local_vars[quad.dest]:
            symbols[var].address_desc_mem.pop()

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

    def ifgoto(self,quad):
        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True)
        save_reg_to_mem(reg1)
        if best_location != reg1:
            print("\tmov " + reg1 + ", " + best_location)
        print("\tcmp " + reg1 + ", 0")
        save_caller_status()
        if(quad.src2.startswith("n")):
            print("\tjne " + quad.dest)
        else:
            print("\tje " + quad.dest)
        
        # reg2 = get_best_location(quad.src2)
        # print("\t" + op + ' ' + reg1 + ", " + reg2)
        # upd_reg_desc(reg1, quad.dest)
        # for sym in reg_desc[reg1]:
        #     dprint(reg1 + ", " + sym)
        # free_all_regs(quad)
        # print("\t")

    def goto(self,quad):
        save_caller_status()
        print("\tjmp " + quad.dest)

    def label(self,quad):
        save_caller_status()
        print(quad.src1 + ":")

    def addr(self, quad):
        reg = get_register(quad)
        print("\tlea " + reg + ", " + get_location_in_memory(quad.src1))
        reg_desc[reg].add(quad.dest)
        symbols[quad.dest].address_desc_reg.add(reg)

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
        elif(quad.op.endswith("_=")):
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
        elif(quad.op.endswith("inc")):
            self.increment(quad)
        elif(quad.op.endswith("dec")):
            self.decrement(quad)
        elif(quad.op.endswith("bitwisenot")):
            self.assign(quad)
            self.bitwisenot(quad)
        elif(quad.op.endswith("uminus")):
            self.assign(quad)
            self.uminus(quad)
        elif(quad.op.split("_")[-1] in relational_op_list):
            self.relational_op(quad)
        elif(quad.op == "ifgoto"):
            self.ifgoto(quad)
        elif(quad.op == "label"):
            self.label(quad)
        elif(quad.op == "goto"):
            self.goto(quad)
        elif(quad.op == "funcEnd"):
            self.funcEnd(quad)
        elif(quad.op.endswith("<<")):
            self.lshift(quad)
        elif(quad.op.endswith(">>")):
            self.rshift(quad)
        elif(quad.op == "addr"):
            self.addr(quad)




def runmain():
    sys.stdout = open('out.asm', 'w')
    codegen = CodeGen()
    codegen.gen_top_headers()
    for quad in instruction_array:
        codegen.generate_asm(quad)
    codegen.data_section()
    sys.stdout.close()
