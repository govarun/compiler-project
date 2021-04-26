from parser import global_symbol_table

register_desc = {}

register_desc["eax"] = set()
register_desc["ebx"] = set()
register_desc["ecx"] = set()
register_desc["edx"] = set()
register_desc["esi"] = set()
register_desc["edi"] = set()
register_desc["ebp"] = set()
register_desc["esp"] = set()

def free_all_regs():
    pass

def get_register(instr_3ac, compulsory = True, exclude_reg = []):
    src1 = instr_3ac[1]
    src2 = instr_3ac[2]
    dest = instr_3ac[3]
    
def save_reg_to_mem():
    pass

def get_location_mem():
    pass

def get_best_location():
    pass




