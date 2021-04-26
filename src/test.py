# for i in range(10, 9, -1):
#     print(i)

#     upd_reg_desc(reg1, quad.src1)

#     def upd_reg_desc(reg, symbol):
#     '''
#         Stores the symbol exclusively in one register, and removes it from other registers
#     '''
#     save_reg_to_mem(reg)
#     if not is_symbol(symbol):
#         return
#     for register in symbols[symbol].address_desc_reg:
#         if register != reg:
#             reg_desc[register].remove(symbol)
#     symbols[symbol].address_desc_reg.clear()
#     symbols[symbol].address_desc_reg.add(reg)
#     reg_desc[reg].add(symbol)
s = "-12232344545"
print(s.is_instance(s, aint))