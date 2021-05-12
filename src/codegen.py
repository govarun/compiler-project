from reg_funcs import *
from helper_functions import *
from parser import symbol_table, local_vars, strings, get_label, label_cnt, global_symbol_table, pre_append_in_symbol_table_list,float_constant_values,float_reverse_map
import sys
diction = {"&&" : "and", "||" : "or", "|" : "or", "&" : "and", "^" : "xor"}
param_count = 0
param_size = 0
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
        for func in pre_append_in_symbol_table_list:
            print("extern " + func)
        print("section .text")
        print("\tglobal main")
        print("main:")
        print("\tpush ebp")
        print("\tmov ebp, esp")

        for var in local_vars['global']:
            # symbols[var].address_desc_mem.append(-4*counter) #why is the first loc variable at ebp -4 and not at ebp
            if(symbols[var].isArray):
                quad = Instruction(0, ['', '', '', ''])
                reg = get_register(quad, compulsory = True)
                print("\tmov " + reg + ", " + str(symbols[var].length))
                # if(symbols[var].isStruct):
                print("\timul " + reg + ", " + str(max(4, get_data_type_size(global_symbol_table[var]['type']))))

                # print("\tshl " + reg + ", 2")
                print("\tpush " + reg)
                print("\tcall malloc")
                print("\tadd esp, 4")
                print("\tmov [" + str(var) + "] , eax")

        for quad in global_instruction_array:
            self.generate_asm(quad)
        save_caller_status()
        print("\tcall _main")

        print("\tmov esp, ebp")
        print("\tpop ebp")
        print("\tret")
        

    def data_section(self):
        print("section\t.data")
        float_tmp_vars = [lis[1] for lis in float_constant_values]
        for vars in local_vars['global']:
            if vars not in strings.keys() and vars not in float_tmp_vars:
                if('value' in global_symbol_table[vars].keys() and not symbols[vars].isArray):
                    print("\t" + vars + "\tdd\t" + str(global_symbol_table[vars]['value']))
                else:
                    print("\t" + vars + "\tdd\t0")
        # print("\tgetInt:\tdb\t\"%d\"\t")
        for name in strings.keys():
            temp_string = (strings[name])[1:-1]
            print("\t" + name + ":\tdb\t`" + temp_string + "`, 0")
        for name in float_constant_values:
            print("\t" + name[1] + "\tdd\t" + name[0])

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

    def real_bin_operations(self,quad,op):

        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True,is_float=True)
        save_reg_to_mem(reg1)
        if best_location != reg1:
            # dprint(best_location + "register printed")
            print("\tmovss " + reg1 + ", " + best_location)
        reg2 = get_best_location(quad.src2)

        print("\t" + op + ' ' + reg1 + ", " + reg2)
        free_all_regs(quad)
        upd_reg_desc(reg1, quad.dest)

    def add(self,quad):
        self.bin_operations(quad, 'add')

    def sub(self, quad):
        self.bin_operations(quad, 'sub')

    def real_add(self,quad):
        self.real_bin_operations(quad,'addss')
    
    def real_sub(self,quad):
        self.real_bin_operations(quad,'subss')

    def mul(self, quad):
        self.bin_operations(quad, 'imul')

    def real_mul(self,quad):
        self.real_bin_operations(quad, 'mulss')

    def real_div(self,quad):
        self.real_bin_operations(quad, 'divss')

    def band(self, quad):
        self.bin_operations(quad, 'and')

    def bor(self, quad):
        self.bin_operations(quad, 'or')
    
    def bxor(self, quad):
        self.bin_operations(quad, 'xor')
    
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

    def relational_float(self,quad):
        best_location = get_best_location(quad.src1)
        reg1 = get_register(quad, compulsory=True,is_float=True)
        save_reg_to_mem(reg1)
        op = quad.op.split("_")[-1]
        if best_location != reg1:
            print("\tmovss " + reg1 + ", " + best_location)
        reg2 = get_best_location(quad.src2)
        reg3 = get_register(quad,compulsory=True)
        print("\t" + "ucomiss" + ' ' + reg1 + ", " + reg2)
        lbl = get_label()
        if(op == "<"):
            print("\tjb " + lbl)
        elif(op == ">"):
            print("\tja " + lbl)
        elif(op == "=="):
            print("\tje " + lbl)
        elif(op == "!="):
            print("\tjne " + lbl)
        elif(op == "<="):
            print("\tjbe " + lbl)
        elif(op == ">="):
            print("\tjae " + lbl)
        print("\tmov " + reg3 + ", 0")
        lbl2 = get_label()
        print("\tjmp " + lbl2)
        print(lbl + ":") 
        print("\tmov " + reg3 + ", 1")
        print(lbl2 + ":")
        upd_reg_desc(reg3, quad.dest)
        free_all_regs(quad)


    def real_assign(self,quad):
        if(quad.src2 is not None):
            #*x = y
            best_location = get_best_location(quad.dest)
            if(best_location not in reg_desc.keys()):
                reg = get_register(quad, compulsory = True)
                print("\tmov " + reg + ", " + best_location)
                #what if best_location is xmm?
                best_location = reg
                
            symbols[quad.dest].address_desc_reg.add(best_location)
            reg_desc[best_location].add(quad.dest)

            if(not is_number(quad.src1)):
                loc = get_best_location(quad.src1)
                if(loc not in reg_desc.keys()):
                    reg = get_register(quad, compulsory = True, exclude_reg = [best_location],is_float = True)
                    upd_reg_desc(reg, quad.src1)
                    print("\tmovss " + reg + ", " + loc)
                    loc = reg
                
                symbols[quad.src1].address_desc_reg.add(loc)
                reg_desc[loc].add(quad.src1)

                print("\tmovss [" + best_location + "], " + loc)
            else:
                print("\tmovss dword [" + best_location + "], " + quad.src1)

            
        elif (is_number(quad.src1)): # case when src1 is an integral numeric
            best_location = get_best_location(quad.dest)
            if (check_type_location(best_location) == "register"):
                upd_reg_desc(best_location, quad.dest)
            print("\tmovss " + best_location + ", " + quad.src1)
        else:
            symbols[quad.dest].pointsTo = symbols[quad.src1].pointsTo
            if(symbols[quad.dest].size <= 4):
                best_location = get_best_location(quad.src1)
                # dprint(quad.src1 + " " + best_location + " " + quad.dest)
                if (best_location not in reg_desc.keys()):
                    reg = get_register(quad, compulsory = True,is_float=True)
                    upd_reg_desc(reg, quad.src1)
                    print("\tmovss " + reg + ", " + best_location)
                    best_location = reg

                symbols[quad.dest].address_desc_reg.add(best_location)
                reg_desc[best_location].add(quad.dest)
                del_symbol_reg_exclude(quad.dest, [best_location])
            else:
                loc1 = get_location_in_memory(quad.dest, sqb = False)
                loc2 = get_location_in_memory(quad.src1, sqb = False)
                reg = get_register(quad, compulsory = True,is_float=True)

                for i in range(0, symbols[quad.dest].size, 4):
                    print("\tmovss " + reg + ", dword [" + loc2 + " + " + str(i) + "]" )
                    print("\tmovss dword [" + loc1 + " + " + str(i) + "], " + reg )

    def assign(self, quad):
        if(quad.src2 is not None):
            #*x = y
            
            if(quad.src1 in symbols.keys() and symbols[quad.src1].size > 4):
                loc1 = get_best_location(quad.dest)
                loc2 = get_location_in_memory(quad.src1, sqb = False)

                if(loc1 not in reg_desc.keys()):
                    reg2 = get_register(quad)
                    print("\tmov " + reg2 + ", "+ loc1)
                    loc1 = reg2

                reg = get_register(quad, exclude_reg = [loc1])

                for i in range(0, symbols[quad.src1].size, 4):
                    print("\tmov " + reg +  ", dword [" + loc2 + " + " + str(i) + "] " )
                    print("\tmov dword [" + loc1 + " + " + str(i) + "], " + reg)


            else:
                best_location = get_best_location(quad.dest)
                if(best_location not in reg_desc.keys()):
                    reg = get_register(quad, compulsory = True)
                    print("\tmov " + reg + ", " + best_location)
                    best_location = reg
                    
                symbols[quad.dest].address_desc_reg.add(best_location)
                reg_desc[best_location].add(quad.dest)

                if(not is_number(quad.src1)):
                    loc = get_best_location(quad.src1)
                    if(loc not in reg_desc.keys()):
                        reg = get_register(quad, compulsory = True, exclude_reg = [best_location])
                        upd_reg_desc(reg, quad.src1)
                        print("\tmov " + reg + ", " + loc)
                        loc = reg
                    
                    symbols[quad.src1].address_desc_reg.add(loc)
                    reg_desc[loc].add(quad.src1)

                    print("\tmov [" + best_location + "], " + loc)
                else:
                    print("\tmov dword [" + best_location + "], " + quad.src1)
            
        elif (is_number(quad.src1)): # case when src1 is an integral numeric
            best_location = get_best_location(quad.dest)
            if (check_type_location(best_location) == "register"):
                upd_reg_desc(best_location, quad.dest)
            print("\tmov " + best_location + ", " + quad.src1)
        else:
            #a = b
            symbols[quad.dest].pointsTo = symbols[quad.src1].pointsTo
            if(symbols[quad.dest].size <= 4):
                best_location = get_best_location(quad.src1)
                # dprint(quad.src1 + " " + best_location + " " + quad.dest)
                if (best_location not in reg_desc.keys()):
                    reg = get_register(quad, compulsory = True)
                    upd_reg_desc(reg, quad.src1)
                    print("\tmov " + reg + ", " + best_location)
                    best_location = reg

                symbols[quad.dest].address_desc_reg.add(best_location)
                reg_desc[best_location].add(quad.dest)
                del_symbol_reg_exclude(quad.dest, [best_location])
            else:
                loc1 = get_location_in_memory(quad.dest, sqb = False)
                loc2 = get_location_in_memory(quad.src1, sqb = False)
                reg = get_register(quad, compulsory = True)

                for i in range(0, symbols[quad.dest].size, 4):
                    print("\tmov " + reg + ", dword [" + loc2 + " + " + str(i) + "]" )
                    print("\tmov dword [" + loc1 + " + " + str(i) + "], " + reg )

            # if (quad.instr_info['nextuse'][quad.src1] == None):
            #     del_symbol_reg_exclude(quad.src1)

    def int2float(self, quad):
        best_location = get_best_location(quad.src1)
        reg = get_register(quad, is_float=True)
        upd_reg_desc(reg,quad.dest)
        print("\tcvtsi2ss " + reg + ", " + best_location)


    def float2int(self, quad):
        best_location = get_best_location(quad.src1)
        reg = get_register(quad, is_float=False)
        upd_reg_desc(reg, quad.dest)
        print("\tcvttss2si " + reg + ", " + best_location)
        #cvtt or cvt? -> [X] Doubt
    
    
    def deref(self, quad):
        #x = *y assignment
        if(len(symbols[quad.src1].pointsTo)> 0):
            sym = symbols[quad.src1].pointsTo
            to_save = []
            while len(sym) > 0:
                to_save.append(sym)
                sym = symbols[sym].pointsTo

            for i in range (len(to_save) -1, -1, -1):
                del_symbol_reg_exclude(to_save[i])

        best_location = get_best_location(quad.src1)
        if (check_type_location(best_location) in ["memory", "data", "number"]):
            reg = get_register(quad, compulsory = True)
            upd_reg_desc(reg, quad.src1)
            print("\tmov " + reg + ", " + best_location)
            best_location = reg

        reg2 = get_register(quad, compulsory  = True, exclude_reg = [best_location])
        print("\tmov " + reg2 + ", [" + best_location + "] ")

        dest_loc = get_best_location(quad.dest)

        if(dest_loc in reg_desc.keys()):
            upd_reg_desc(dest_loc, quad.dest)

        print("\tmov " + dest_loc + ", " + reg2 )

    def param(self, quad):
        global param_count
        global param_size
        if(param_count == 0):
            save_caller_status()
        param_count += 1
        param_size += 4
        if(is_symbol(quad.src1) and symbols[quad.src1].size > 4):
            param_size += symbols[quad.src1].size - 4
            loc = get_location_in_memory(quad.src1, sqb = False)
            for i in range(symbols[quad.src1].size - 4, -1, -4):
                print("\tpush dword [" + loc + "+" + str(i) + "]")
            return
        location = get_best_location(quad.src1)
        if(is_symbol(quad.src1) and global_symbol_table[quad.src1]['type'] == 'float' and quad.dest == 'printf'):
            if(location.startswith('xmm')):
                save_reg_to_mem(location)
            print("\tsub\tesp, 8")
            reg1 = get_register(quad,compulsory=True)
            if(is_symbol(quad.src1)):
                print("\tlea " + reg1 + ", " + get_location_in_memory(quad.src1))
            else:
                print("\tmov " + reg1 + ", " + float_reverse_map[quad.src1])
            print("\tfld dword [" + reg1 + "]")
            print("\tfstp qword [esp]")
            #after pushing float do we need to add 8 or 4
        else:  
            if(location.startswith('xmm')):
                del_symbol_reg_exclude(quad.src1)
            print("\tpush " + get_best_location(quad.src1))

    def function_call(self, quad):
        global param_count, param_size
        save_caller_status()
        if(len(quad.src2) and symbols[quad.src2].size > 4):
            #idhar koi haath mat lagana
            print("\tmov ecx, ebp")
            print("\tsub ecx, esp")
            print("\tadd ecx, " + str(symbols[quad.src2].address_desc_mem[-1]+ 12))
            print("\tpush ecx")
            #####
            param_size += 4
            param_count += 1
        print("\tcall " + quad.src1)

        if(len(quad.src2) and symbols[quad.src2].size <= 4):
            print("\tmov " + get_best_location(quad.src2) + ", eax")
        print("\tadd esp, " + str(param_size))
        param_count = 0
        param_size = 0

    def funcEnd(self, quad):
        for var in local_vars[quad.dest]:
            symbols[var].address_desc_mem.pop()
        #do we need to do this?
        for key in reg_desc.keys():
            reg_desc[key].clear()

    def alloc_stack(self,quad):
        '''
        Allocate stack space for function local variables
        '''
        if(quad.src1 == 'main'):
            print("_main:")
        else:
            print(quad.src1 + ":")
        offset = 0
        for var in local_vars[quad.src1]:
            if var not in func_arguments[quad.src1]:
                # dprint(var + " " + str(-offset))
                offset += get_data_type_size(global_symbol_table[var]['type'])
                symbols[var].address_desc_mem.append(-offset) #why is the first loc variable at ebp -4 and not at ebp`

        print("\tpush ebp")
        print("\tmov ebp, esp")
        print("\tsub esp, " + str(offset))

        for var in local_vars[quad.src1]:
            if var not in func_arguments[quad.src1]:
                # symbols[var].address_desc_mem.append(-4*counter) #why is the first loc variable at ebp -4 and not at ebp
                if(symbols[var].isArray):
                    reg = get_register(quad, compulsory = True)
                    print("\tmov " + reg + ", " + str(symbols[var].length))
                    # if(symbols[var].isStruct):
                    print("\timul " + reg + ", " + str(max(4, get_data_type_size(global_symbol_table[var]['type']))))

                    # print("\tshl " + reg + ", 2")
                    print("\tpush " + reg)
                    print("\tcall malloc")
                    print("\tadd esp, 4")
                    print("\tmov " + get_location_in_memory(var) + ", eax")

        counter = 0
        if(get_data_type_size(symbol_table[0][quad.src1]['type']) > 4):
            counter += 4
        for var in func_arguments[quad.src1]:
            symbols[var].address_desc_mem.append(counter + 8)
            if(symbols[var].isArray):
                counter += 4
            else:
                counter += symbols[var].size


    # def handle_pointer(self,quad):
    #     reg1 = get_best_location(quad.)


    def function_return(self, quad):
        save_caller_status()
        if(quad.src1):
            if(is_symbol(quad.src1) and symbols[quad.src1].size > 4):
                loc2 = get_location_in_memory(quad.src1, sqb = False)
                print("\tmov eax, dword [ebp + 8]")
                loc1 = "ebp + eax"
                reg = get_register(quad, exclude_reg = ["eax"])

                for i in range(0, symbols[quad.src1].size, 4):
                    print("\tmov " + reg + ", dword [" + loc2 + " + " + str(i) + "]" )
                    print("\tmov dword [" + loc1 + " + " + str(i) + "], " + reg )
            else:
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
        if(symbols[quad.src1].isArray):
            if(reg != get_best_location(quad.src1)):
                print("\tmov " + reg + ", " + get_best_location(quad.src1))
        else:
            if(len(symbols[quad.src1].address_desc_reg)):
                del_symbol_reg_exclude(quad.src1)
            print("\tlea " + reg + ", " + get_location_in_memory(quad.src1))
        symbols[quad.dest].pointsTo = quad.src1
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
        elif(quad.op == "int2float"):
            self.int2float(quad)
        elif(quad.op == "float2int"):
            self.float2int(quad)
        elif(quad.op == "float_="):
            self.real_assign(quad)
        elif(quad.op.endswith("_=")):
            self.assign(quad)
        elif(quad.op == "ret"):
            self.function_return(quad)
        elif(quad.op == "float_+"):
            self.real_add(quad)
        elif(quad.op.endswith("+")): # matches with everything other than real_+
            self.add(quad)
        elif(quad.op == "float_-"):
            self.real_sub(quad)
        elif(quad.op == "float_*"):
            self.real_mul(quad)
        elif(quad.op == "float_/"):
            self.real_div(quad)
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
        elif(quad.op == "float_uminus"):
            self.assign(quad)
            self.real_uminus(quad)
        elif(quad.op.endswith("uminus")):
            self.assign(quad)
            self.uminus(quad)
        elif(quad.op.split("_")[-1] in relational_op_list and quad.op.startswith("int")):
            self.relational_op(quad)
        elif(quad.op.split("_")[-1] in relational_op_list and quad.op.startswith("float")):
            self.relational_float(quad)
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
        elif(quad.op == "deref"):
            self.deref(quad)
        elif(quad.op.endswith("&")):
            self.band(quad)
        elif(quad.op.endswith("|")):
            self.bor(quad)
        elif(quad.op.endswith("^")):
            self.bxor(quad)



def runmain():
    sys.stdout = open('out.asm', 'w')
    codegen = CodeGen()
    codegen.gen_top_headers()
    for quad in instruction_array:
        codegen.generate_asm(quad)
    codegen.data_section()
    sys.stdout.close()
