from helper_functions import *
from parser import local_vars, strings
import copy

# 32 bit register descriptors
reg_desc = {}
reg_desc["eax"] = set()
reg_desc["ebx"] = set()
reg_desc["ecx"] = set()
reg_desc["edx"] = set()
reg_desc["esi"] = set()
reg_desc["edi"] = set()


def free_all_regs(instr):
    '''
        Frees the  src1, src2 registers of an instruction based on whether they are used ahead or not
    '''
    to_free = [instr.src1, instr.src2] # the dest is not to be freed
    for operand in to_free:
        if (operand != None and is_symbol(operand) and instr.instr_info['nextuse'][operand] == None
            and instr.instr_info['live'][operand] == False):
            temp_reg=''
            for reg in symbols[operand].address_desc_reg:
                reg_desc[reg].remove(operand)
                temp_reg = reg
            symbols[operand].address_desc_reg.clear()
            if temp_reg != '':
                print("\tmov dword " + get_location_in_memory(operand) + ", " + temp_reg)




def get_register(instr, compulsory = True, exclude_reg = []):
    '''
        Function to get the best register for instr.dest, using nextuse and live status of the symbols
        X := Y op Z
    '''
    if is_symbol(instr.src1): 
        for reg in symbols[instr.src1].address_desc_reg:
            if reg not in exclude_reg:
                if(len(reg_desc[reg]) == 1 and instr.instr_info['nextuse'][instr.src1] == None\
                and not instr.instr_info['live'][instr.src1]):
                    # symbols[instr.src1].address_desc_reg.remove(reg)
                    # upd_reg_desc(reg, instr.dest)
                    save_reg_to_mem(reg)
                    return reg

    for reg in reg_desc.keys():
        if(reg not in exclude_reg):
            if(len(reg_desc[reg]) == 0):
                # upd_reg_desc(reg, instr.dest)
                save_reg_to_mem(reg)
                return reg
    
    if(instr.instr_info['nextuse'][instr.dest] != None or compulsory == True):
        '''
        This part returns the register which contains the value
        of minimum number of symbols
        '''
        R = None
        for reg in reg_desc.keys():
            if(reg not in exclude_reg):
                if(R == None):
                    R = reg
                elif(len(reg_desc[reg]) < len(reg_desc[R])):
                    R = reg
        # upd_reg_desc(R,instr.dest)
        save_reg_to_mem(R)
        return R

    else:
        return get_location_in_memory(instr.dest)

def save_reg_to_mem(reg):
    '''
    Function to save the contents of a register to memory
    '''
    saved_loc = set()
    for symbol in reg_desc[reg]:
        location = get_location_in_memory(symbol)
        if location not in saved_loc:
            print("\tmov dword " + get_location_in_memory(symbol) + ", " + reg)
            saved_loc.add(location)
        symbols[symbol].address_desc_reg.remove(reg)
    reg_desc[reg].clear()

def get_location_in_memory(symbol):
    '''
    Function to get the location of a symbol in memory
    '''
    if (symbol.startswith('__')):
        return "[" + str(symbol) + "]"
    location = symbols[symbol].address_desc_mem[-1]
    prefix_string = "["
    if(is_number(location)):   # changed this from type(location) is int to .isnumeric
        prefix_string = "[ebp"
        if(location >= 0):
            prefix_string = "[ebp+"
    return prefix_string+str(location)+"]"

def save_caller_status():
    '''
    Function to save the status of the caller function
    '''
    saved = set()
    for reg in reg_desc.keys():
        for symbol in reg_desc[reg]:
            if symbol not in saved:
                print("\tmov dword " +  get_location_in_memory(symbol) + ", " + reg)
                saved.add(symbol)
                symbols[symbol].address_desc_reg.clear()
        reg_desc[reg].clear()


def get_best_location(symbol, exclude_reg = []):
    '''
        Gives the best location for a symbol:
        - for global symbols it gives it in data section
        - for symbols in register it gives the register name
        - for remaining symbols it gives the memory location
    '''
    if is_number(symbol):
        return symbol
    if(symbol in strings.keys()):
        return symbol
    if is_symbol(symbol):
        for reg in symbols[symbol].address_desc_reg:
            if (reg not in exclude_reg):
                return reg
    if(symbol.isnumeric()):
        return symbol
    return "dword " + get_location_in_memory(symbol)

def check_type_location(location):
    if is_number(location):
        return 'number'
    elif (location.startswith('[')):
        return "memory"
    elif(location.startswith("dword")):
        return "data"
    else:
        return "register"

def del_symbol_reg_exclude(symbol, exclude = []):
    '''
        Delete symbol from all registers excule the ones in the list
    '''
    to_keep = set()
    for reg in symbols[symbol].address_desc_reg:
        if reg not in exclude:
            reg_desc[reg].remove(symbol)
        else:
            to_keep.add(reg)
    symbols[symbol].address_desc_reg.clear()
    symbols[symbol].address_desc_reg = copy.deepcopy(to_keep)

def upd_reg_desc(reg, symbol):
    '''
        Stores the symbol exclusively in one register, and removes it from other registers
    '''
    save_reg_to_mem(reg)
    if not is_symbol(symbol):
        return
    for register in symbols[symbol].address_desc_reg:
        if register != reg:
            reg_desc[register].remove(symbol)
    symbols[symbol].address_desc_reg.clear()
    symbols[symbol].address_desc_reg.add(reg)
    reg_desc[reg].add(symbol)


