import re

def parse_format_string(format_str):
    c_reg_exp='''\
    %                                  # literal "%"
    (?:                                # first option
    (?:[-+0 #]{0,5})                   # optional flags
    (?:\d+|\*)?                        # width
    (?:\.(?:\d+|\*))?                  # precision
    (?:h|l|ll|w|I|I32|I64)?            # size
    ([cCdiouxXeEfgGaAnpsSZ])             # type
    ) |                                # OR
    %%                                # literal "%%"
    '''
    types=[]
    type_dict = {"x": ["int", "int *", "char *", "float*"],\
                "d": ["int"],\
                "f": ["float"]}
    for match in re.finditer(c_reg_exp, format_str, flags = re.X):
        types.append(match.group(1))
    types = [type for type in types if type is not None]
    return types

# format_str = "Hello \%d %f hhe %x jksdj %lld %llx %ld"
format_str = "Hello %%d %%d %%d %d %x %%d%f"
print(parse_format_string(format_str))