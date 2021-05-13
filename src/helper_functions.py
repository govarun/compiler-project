import pprint
from parser import *
import sys
instruction_array = []
global_instruction_array = []
leaders = [0]
nextuse = {}
live = {}
symbols = {}


class symbol_info:
    def __init__(self, isArray = False, length = 0, isStruct = False, size = 0, pointsTo = ''):
        self.isArray = isArray
        self.isStruct = isStruct
        self.size = ((size + 3)//4)*4
        self.length = length
        self.address_desc_mem = []
        self.pointsTo = pointsTo
        self.address_desc_reg = set()

class Instruction:
    def __init__(self,lno,quad):
        self.lno = lno
        self.src1 = None
        self.src2 = None
        self.dest = None
        self.jump_label = None
        self.op = None # instr_type
        self.instr_info = {}
        self.instr_info['nextuse'] = {}
        self.instr_info['live'] = {}
        self.argument_list = []
        self.fill_info(quad)

    def fill_info(self,quad):
        self.op = quad[0]
        if(self.op == "ifgoto"):
            self.dest = quad[3]
            self.src1 = quad[1]
            self.src2 = quad[2] # should change?
            print("ifgoto : ", self.src1 , self.src2 , self.dest) #check this

        # elif(self.op.split("_")[-1] in relational_op_list):
        #     self.dest = quad[3]
        #     self.src1 = quad[1]
        #     self.src2 = quad[2]

        elif(self.op == "goto"):
            self.dest = quad[3]
            print("goto : ", self.dest) 

        elif(self.op == "inc" or self.op == "dec"):
            if(global_symbol_table[quad[3]]['type'] == 'float'):
                if(self.op == 'inc'):
                    self.op = 'float_+'
                else:
                    self.op = 'float_-'
                self.src1 = quad[3]
                self.src2 = float_reverse_map["1.0"]
                self.dest = quad[3]
                if(self.op == 'inc'):
                    print(self.dest, "=", self.src1, "float_+ 1.0") 
                else:
                    print(self.dest, "=", self.src1, "float_- 1.0") 
            else:    
                self.src1 = quad[3]
                print(self.op, self.dest)
                    
                    


        elif(self.op.endswith('bitwisenot')):
            self.src1 = quad[1]
            self.dest = quad[3]
            print(self.dest, "= ~", self.src1) 

        elif(self.op == "param"):
            self.src1 = quad[3]
            self.dest = quad[2]
            print(self.op, self.src1)

        elif(self.op == "ret"):
            if(quad[3] != ""):
                self.src1 = quad[3]
            print(self.op, quad[3])

        elif(self.op == "func"):
            self.src1 = quad[3]
            print(self.op , self.src1)

        elif(self.op == "call"):
            self.src1 = quad[3]
            self.src2 = quad[2]
            print(self.op, quad[1], quad[2], quad[3])
        
        elif(self.op == "int_float_="):
            self.op = "int2float"
            self.src1 = quad[1]
            self.dest = quad[3]
            print(self.dest, "=" , self.op , self.src1)
        
        elif(self.op == "float_int_="):
            self.op = "float2int"
            self.src1 = quad[1]
            self.dest = quad[3]
            print(self.dest, "=" , self.op , self.src1)
        
        elif(self.op == "char_int_="):
            self.op = "char2int"
            self.src1 = quad[1]
            self.dest = quad[3]
            print(self.dest, "=" , self.op , self.src1)

        elif(self.op == "char_float_="):
            self.op = "char2float"
            self.src1 = quad[1]
            self.dest = quad[3]
            print(self.dest, "=" , self.op , self.src1)
        
        elif(self.op == "int_char_="):
            self.op = "int2char"
            self.src1 = quad[1]
            self.dest = quad[3]
            print(self.dest, "=" , self.op , self.src1)

        elif(self.op == "float_char_="):
            self.op = "float2char"
            self.src1 = quad[1]
            self.dest = quad[3]
            print(self.dest, "=" , self.op , self.src1)

        elif(self.op == "int_=" or self.op == "int_int_=" or self.op == "float_=" or self.op == "char_=" or self.op == "char_char_="):
            self.dest = quad[3]
            self.src1 = quad[1]
            if (quad[2] != ''):
                self.src2 = quad[2]
                print(self.dest, self.op, self.src2, self.src1)
            else:
                print(self.dest, self.op , self.src1)

        elif(self.op == "label"):
            self.src1 = quad[3]
            print(self.op, self.src1)

        elif(self.op == "int_uminus"):
            self.dest = quad[3]
            self.src1 = quad[1]
            print(self.dest, "int_= -", self.src1)

        elif(self.op == "float_uminus"):
            self.dest = quad[3]
            self.src1 = quad[1]
            self.src2 = float_reverse_map["-1.0"]
            self.op = "float_*"
            print(self.dest, "float_= -", self.src1)

        elif(self.op.startswith("int_") or self.op.startswith("float_") or self.op.startswith("char_")):
            self.dest = quad[3]
            self.src1 = quad[1]
            self.src2 = quad[2]
            print(self.dest, "=", self.src1 , self.op , self.src2)

        elif(self.op == "addr"):
            self.dest = quad[3]
            self.src1 = quad[1]
            print(self.dest, "= addr", self.src1)

        elif(self.op == "*"):
            self.op = "deref"
            self.dest = quad[3]
            self.src1 = quad[1]
            print(self.dest, "= deref", self.src1)
        
        elif(self.op == "funcEnd"):
            self.dest = quad[3]
            print(self.op) 

def find_basic_blocks():
    i = 1
    for quads in global_emit_array:
        instruction = Instruction(i,quads)
        global_instruction_array.append(instruction)

    for quads in emit_array:
        instruction = Instruction(i,quads)
        instruction_array.append(instruction)
        op = quads[0] # assuming 0 is always instruction name
        extra = 0
        if(op in ["label","goto","ifgoto","ret","call","func","funcEnd"]):
            if(op != "label" and op != "func"):
                extra += 1
            leaders.append(i - 1 + extra)
        i += 1
    leaders.append(len(emit_array))
    # print(leaders)
    # print(instruction_array)

def is_symbol(var):
    if(var in global_symbol_table.keys()):
        return True
    else:
        return False

def is_number(number):
    number = str(number)
    if (number.startswith('-')):
        return True
    if number[0] == '.' or number[0].isnumeric():
        return True
    return False

def gen_next_use_and_live():

    sz = len(global_instruction_array)
    for j in range(0, sz): # doing forwards pass and filling default values
        cur_instr = global_instruction_array[j]
        src1, src2, dest = cur_instr.src1, cur_instr.src2, cur_instr.dest
        for operand in [src1, src2, dest]:
            if (operand != None and not operand.isnumeric()):
                live[operand] = False
                nextuse[operand] = None

    for j in range(sz-1, -1, -1): # backward pass to set next use and live
        # print(block_end, block_start, j)
        cur_instr = global_instruction_array[j]
        src1, src2, dest = cur_instr.src1, cur_instr.src2, cur_instr.dest
        
        if (dest != None and not dest.isnumeric() and is_symbol(dest)):
            cur_instr.instr_info['live'][dest] = live[dest]
            cur_instr.instr_info['nextuse'][dest] = nextuse[dest]
            live[dest] = False
            nextuse[dest] = None
        if (src2 != None and not src2.isnumeric() and is_symbol(src2)):
            cur_instr.instr_info['live'][src2] = live[src2]
            cur_instr.instr_info['nextuse'][src2] = nextuse[src2]
            live[src2] = True
            nextuse[src2] = j
        if (src1 != None and not src1.isnumeric() and is_symbol(src1)):
            cur_instr.instr_info['live'][src1] = live[src1]
            cur_instr.instr_info['nextuse'][src1] = nextuse[src1]
            live[src1] = True
            nextuse[src1] = j

    for i in range(len(leaders) - 1):
        ignore_instr_list = ['param']
        block_start = leaders[i] # just the instruction next to the leader
        block_end = leaders[i + 1] - 1 # instruction previous to the next leader


        for j in range(block_start, block_end + 1): # doing forwards pass and filling default values
            cur_instr = instruction_array[j]
            src1, src2, dest = cur_instr.src1, cur_instr.src2, cur_instr.dest
            for operand in [src1, src2, dest]:
                if (operand != None and not operand.isnumeric()):
                    live[operand] = False
                    nextuse[operand] = None

        for j in range(block_end, block_start - 1, -1): # backward pass to set next use and live
            # print(block_end, block_start, j)
            cur_instr = instruction_array[j]
            src1, src2, dest = cur_instr.src1, cur_instr.src2, cur_instr.dest
            if cur_instr.op in ignore_instr_list:
                continue
            if (dest != None and not dest.isnumeric() and is_symbol(dest)):
                cur_instr.instr_info['live'][dest] = live[dest]
                cur_instr.instr_info['nextuse'][dest] = nextuse[dest]
                live[dest] = False
                nextuse[dest] = None
            if (src2 != None and not src2.isnumeric() and is_symbol(src2)):
                cur_instr.instr_info['live'][src2] = live[src2]
                cur_instr.instr_info['nextuse'][src2] = nextuse[src2]
                live[src2] = True
                nextuse[src2] = j
            if (src1 != None and not src1.isnumeric() and is_symbol(src1)):
                cur_instr.instr_info['live'][src1] = live[src1]
                cur_instr.instr_info['nextuse'][src1] = nextuse[src1]
                live[src1] = True
                nextuse[src1] = j
            # print("Instruction: " + str(emit_array[j]))
            # pprint.pprint(cur_instr.instr_info)



def print_basic_blocks(debug = False):
    print("\n###### LEADERS ######")
    print(leaders)
    # print(instruction_array)
        
def runmain():
    sys.stdout = open('3ac_output.txt', 'w')
    find_basic_blocks()
    gen_next_use_and_live()
    for key in global_symbol_table.keys():
        if key not in symbols.keys():
            if('array' in global_symbol_table[key].keys()):
                len = global_symbol_table[key]['size']//get_data_type_size(global_symbol_table[key]['type'])
                symbols[key] = symbol_info(isArray = True, length = len)
            elif(global_symbol_table[key]['type'].startswith('struct') or global_symbol_table[key]['type'].startswith('union')):
                symbols[key] = symbol_info(isStruct = True, size = get_data_type_size(global_symbol_table[key]['type']))
            else:
                symbols[key] = symbol_info(size = get_data_type_size(global_symbol_table[key]['type']))
    sys.stdout.close()
    # print_basic_blocks(debug = True)



