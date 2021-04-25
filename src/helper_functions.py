from parser import emit_array
instruction_array = []
leaders = [1]
class Instruction:
    def __init__(self,lno,quad):
        self.lno = lno
        self.src1 = None
        self.src2 = None
        self.dest = None
        self.jump_label = None
        self.op = None # instr_type
        self.instruc_info = {}
        self.fill_info(quad)

    def fill_info(self,quad):
        self.op = quad[0]
        if(self.op == "ifgoto"):
            self.dest = quad[3]
            self.src1 = quad[1]
            self.src2 = quad[2] # should change?
        
        elif(self.op == "goto"):
            self.dest = quad[3]
        
        elif(self.op == "inc" or self.op == "dec"): # exists?
            pass
        
        elif(self.op == "param"):
            self.dest = quad[3]
        
        elif(self.op == "ret"):
            if(quad[3] != ""):
                self.dest = quad[3]

        elif(self.op == "func"):
            self.dest = quad[3]

        elif(self.op == "int_="):
            self.dest = quad[3]
            self.src1 = quad[1]
        
        elif(self.op == "label"):
            self.dest = quad[3]
        
        elif(self.op == "int_uminus"):
            self.dest = quad[3]
            self.src1 = quad[1]

        elif(self.op.startswith("int_")):
            self.dest = quad[3]
            self.src1 = quad[1]
            self.src2 = quad[2]
        
        elif(self.op == "addr"):
            self.dest = quad[3]
            self.src1 = quad[1]

        elif(self.op == "*"):
            self.dest = quad[3]
            self.src1 = quad[1]
        


def find_basic_blocks():
    i = 1
    for quads in emit_array:
        instruction = Instruction(i,quads)
        instruction_array.append(instruction)
        op = quads[0] # assuming 0 is always instruction name
        if(op in ["label","goto","ifgoto","ret","call","func","funcEnd"]):
            # cannot understand fully
            leaders.append(i)
        i += 1
    leaders.append(len(emit_array)+1)
    # print(leaders)
    # print(instruction_array)

