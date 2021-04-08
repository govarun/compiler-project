# Yacc example

import ply.yacc as yacc
import sys
import pydot
import copy
import json

# Get the token map from the lexer.  This is required.
from lexer import tokens
precedence = (
     ('nonassoc', 'IFX'),
     ('nonassoc', 'ELSE')
 )

# in scope name, 0 denotes global, 1 denotes loop and 2 denotes if/switch, 3 denotes function
curType = []
curFuncReturnType = ''
symbol_table = []
symbol_table.append({})
# typedef_list = {}
# all_typedef = []
currentScope = 0
nextScope = 1
parent = {}
parent[0] = 0
loopingDepth = 0
switchDepth = 0
size={}
size['int'] = 4
size['char'] = 1
size['float'] = 4


class Node:
  def __init__(self,name = '',val = '',lno = 0,type = '',children = '',scope = 0, array = [], maxDepth = 0,isFunc = 0, parentStruct = '', level = 0,ast = None):
    self.name = name
    self.val = val
    self.type = type
    self.lno = lno
    self.scope = scope
    self.array = array
    self.maxDepth = maxDepth
    self.isFunc = isFunc
    self.parentStruct = parentStruct
    self.ast = ast
    self.level = level
    if children:
      self.children = children
    else:
      self.children = []
    
    # add more later
ts_unit = Node('START',val = '',type ='' ,children = [])

def get_higher_data_type(type_1 , type_2):
  if(type_1.endswith('*')):
    return type_1
  if(type_2.endswith('*')):
    return type_2
  to_num = {}
  to_num['char'] = 0
  to_num['short'] = 1
  to_num['int'] = 2
  to_num['long'] = 3 
  to_num['float'] = 4
  to_num['double'] = 5
  to_str = {}
  to_str[0] = 'char'
  to_str[1] = 'short' 
  to_str[2] = 'int'
  to_str[3] = 'long'
  to_str[4] = 'float'
  to_str[5] = 'double'
  type_1 =  type_1.split()[-1]
  type_2 =  type_2.split()[-1]
  if (type_1 not in to_num) or type_2 not in to_num:
    return str(-1)
  num_type_1 = to_num[type_1]
  num_type_2 = to_num[type_2]
  return to_str[max(num_type_1 , num_type_2)]

def get_data_type_size(type_1):
  # print(type_1)
  type_size = {}
  type_size['char'] = 1
  type_size['short'] = 2
  type_size['int'] = 4
  type_size['long'] = 8
  type_size['float'] = 4
  type_size['double'] = 8
  type_size['void'] = 0
  if(type_1.endswith('*')):
    return 8
  if( type_1.startswith('struct') or type_1.startswith('union')):
    curscp = currentScope
    while(parent[curscp] != curscp):
      if(type_1 in symbol_table[curscp].keys()):
        break
      curscp = parent[curscp]
    if (curscp == 0):
      if(type_1 not in symbol_table[curscp].keys()):
        return -1 # If id is not found in symbol table
    return symbol_table[curscp][type_1]['size']    
  type_1 = type_1.split()[-1]
  if type_1 not in type_size.keys():
    return -1
  return type_size[type_1]
  
  

def ignore_1(s):
  if(s == "}"):
    return True
  elif(s == "{"):
    return True
  elif(s == ")"):
    return True
  elif(s == "("):
    return True
  elif(s == ";"):
    return True
  elif(s == '['):
    return True
  elif(s == ']'):
    return True
  elif(s == ','):
    return True
  return False

def find_if_ID_is_declared(id,lineno):
  curscp = currentScope
  # print("here" + str(curscp))
  while(parent[curscp] != curscp):
    # print("here" + str(curscp))
    if(id in symbol_table[curscp].keys()):
      return curscp
    curscp = parent[curscp]
  if (curscp == 0):
    if(id in symbol_table[curscp].keys()):
      return curscp
  print (lineno, 'COMPILATION ERROR: unary_expression ' + id + ' not declared')
  return -1


def find_scope(id, lineno):
  curscp = currentScope
  # print("here" + str(curscp))
  while(parent[curscp] != curscp):
    # print("here" + str(curscp))
    if(id in symbol_table[curscp].keys()):
      return curscp
    curscp = parent[curscp]
  if (curscp == 0):
    if(id in symbol_table[curscp].keys()):
      return curscp
  return -1


cur_num = 0

def build_AST(p,nope = []):
  global cur_num
  calling_func_name = sys._getframe(1).f_code.co_name
  calling_rule_name = calling_func_name[2:]
  length = len(p)
  if(length == 2):
    if(type(p[1]) is Node):
      # print(p[1].ast,p[0].name)
      return p[1].ast
    else:
      # print(p[1],p[0].name)
      return p[1]
  else:
    cur_num += 1
    p_count = cur_num
    open('graph1.dot','a').write("\n" + str(p_count) + "[label=\"" + calling_rule_name.replace('"',"") + "\"]") ## make new vertex in dot file
    for child in range(1,length,1):
      if(type(p[child]) is Node and p[child].ast is None):
        continue
      global child_num 
      global child_val
      if(type(p[child]) is not Node):
        if(type(p[child]) is tuple):
          if(ignore_1(p[child][0]) is False):
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child][1]))
        else:
          if(ignore_1(p[child]) is False):
            cur_num += 1
            open('graph1.dot','a').write("\n" + str(cur_num) + "[label=\"" + str(p[child]).replace('"',"") + "\"]")
            p[child] = (p[child],cur_num)
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child][1]))
      else:
        if(type(p[child].ast) is tuple):
          if(ignore_1(p[child].ast[0]) is False):
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child].ast[1]))
        else:
          if(ignore_1(p[child].ast) is False):
            cur_num += 1
            open('graph1.dot','a').write("\n" + str(cur_num) + "[label=\"" + str(p[child].ast).replace('"',"") + "\"]")
            p[child].ast = (p[child].ast,cur_num)
            open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child].ast[1]))

    return (calling_rule_name,p_count)


def p_primary_expression_0(p):
  '''primary_expression : ID'''
  p[0] = Node(name = 'PrimaryExpression',val = p[1],lno = p.lineno(1),type = '',children = [])
  temp = find_if_ID_is_declared(p[1],p.lineno(1))
  if(temp != -1):
    # if('type' in symbol_table[temp][p[1]]):
    p[0].type = symbol_table[temp][p[1]]['type']
    if('array' in symbol_table[temp][p[1]].keys()):
      p[0].level = len(symbol_table[temp][p[1]]['array'])
    if('isFunc' in symbol_table[temp][p[1]]):
      p[0].isFunc = 1
    p[0].ast = build_AST(p)

def p_primary_expression_1(p):
  '''primary_expression : OCTAL_CONST
                | HEX_CONST
                | BIN_CONST
                | LPAREN expression RPAREN
  '''
  # p[0] = build_AST(p)
  if(len(p) == 4):
    p[0] = p[2]
    p[0].ast = build_AST(p,[1,3])
    # p[0].name = 'primaryExpression'
  else:
    p[0] = Node(name = 'PrimaryExpression',val = p[1],lno = p.lineno(1),type = '',children = [])
    

def p_primary_expression_2(p):
  '''primary_expression : CHAR_CONST'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'char',children = [])
  p[0].ast = build_AST(p)

def p_primary_expression_3(p):
  '''primary_expression : INT_CONST'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'int',children = [])
  p[0].ast = build_AST(p)

def p_primary_expression_4(p):
  '''primary_expression : FLOAT_CONST'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'float',children = [])
  p[0].ast = build_AST(p)

def p_primary_expression_5(p):
  '''primary_expression : STRING_LITERAL'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'string',children = [])
  p[0].ast = build_AST(p)

########################

def p_postfix_expression_1(p):
  '''postfix_expression : primary_expression'''
  #p[0] = Node()
  # p[0] = build_AST(p)
  p[0] = p[1]
  p[0].ast = build_AST(p)

def p_postfix_expression_2(p):
  '''postfix_expression : postfix_expression LSQUAREBRACKET expression RSQUAREBRACKET'''
  # check if value should be p[1].val
  p[0] = Node(name = 'ArrayExpression',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1],p[3]],isFunc=p[1].isFunc, parentStruct = p[1].parentStruct)
  p[0].array = copy.deepcopy(p[1].array)
  p[0].array.append(p[3].val)
  p[0].level = p[1].level - 1
  tempScope = find_scope(p[1].val, p.lineno(1))
  p[0].ast = build_AST(p)
  # if(len(p[0].array) > 0 and len(p[0].parentStruct) == 0 and (('array' not in symbol_table[tempScope][p[0].val].keys() and len(p[0].array) == 1) or len(symbol_table[tempScope][p[0].val]) == len(p[0].array) + 1)):
  #     print('COMPILATION ERROR at line ' + str(p[1].lno) + ' , dimensions not specified correctly for ' + p[1].val)
  # if(len(p[0].parentStruct) > 0):
  #   found_scope = find_scope(p[0].parentStruct , p[1].lno)
  #   for curr_list in symbol_table[found_scope][p[0].parentStruct]['field_list']:
  #     # print(curr_list)
  #     if curr_list[1] == p[0].val:
  #       if(len(curr_list) < 5 and len(p[0].array) == 0):
  #         break
  #       if(len(curr_list) < 5 or (len(curr_list[4]) == len(p[0].array) - 1)):
  #         print("COMPILATION ERROR at line ", str(p[1].lno), ", incorrect number of dimensions specified for " + p[1].val)
  if(p[0].level == -1):
    print("COMPILATION ERROR at line ", str(p[1].lno), ", incorrect number of dimensions specified for " + p[1].val)


  curscp = currentScope
  if(p[3].type not in ['char', 'short', 'int', 'long']):
    print("Compilation Error: Array index at line ", p[3].lno, " is not of compatible type")

def p_postfix_expression_3(p):
  '''postfix_expression : postfix_expression LPAREN RPAREN'''
  p[0] = Node(name = 'FunctionCall1',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1]],isFunc=0)
  p[0].ast = build_AST(p,[2,3])
  if(p[1].val not in symbol_table[0].keys() or 'isFunc' not in symbol_table[0][p[1].val].keys()):
    print('COMPILATION ERROR at line ' + str(p[1].lno) + ': no function with name ' + p[1].val + ' declared')
  elif(len(symbol_table[0][p[1].val]['argumentList']) != 0):
    print("Syntax Error at line",p[1].lno,"Incorrect number of arguments for function call")  
  
# def compare_types(call_type,argument):
#   if(call_type == '' or argument == ''):
#     return -1
#   if(call_type.endswith('*')):
#     if(not argument.endswith('*')):
#       return -1
#     return 1
#   if(call_type.startswith('const')):
#     if(not argument.startswith('const')):
#       return -1
  
#   type_1 = call_type.split()[-1]
#   type_2 = argument.split()[-1]
#   # if(type_1 == 'int'):


def p_postfix_expression_4(p):
  '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
  p[0] = Node(name = 'FunctionCall2',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [],isFunc=0)
  # print(p[1].val)
  p[0].ast = build_AST(p,[2,4])
  if(p[1].val not in symbol_table[0].keys() or 'isFunc' not in symbol_table[0][p[1].val].keys()):
    print('COMPILATION ERROR at line :' + str(p[1].lno) + ': no function with name ' + p[1].val + ' declared')
  elif(len(symbol_table[0][p[1].val]['argumentList']) != len(p[3].children)):
    print("Syntax Error at line " + str(p[1].lno) + " Incorrect number of arguments for function call")
  else:
    i = 0
    # curScope = symbol_table[0][p[1].val]['FunctionScope']
    for arguments in symbol_table[0][p[1].val]['argumentList']:
      # print(p[3].children[i].val)
      curVal = p[3].children[i].val
      if(curVal not in symbol_table[currentScope].keys()):
        continue
      curType = symbol_table[currentScope][curVal]['type']
      # temp = compare_types(curType,arguments)
      if(curType.split()[-1] != arguments.split()[-1]):
        print("warning at line " + str(p[1].lno), ": Type mismatch in argument " + str(i+1) + " of function call, " + 'actual type : ' + arguments + ', called with : ' + curType)
      i += 1
  #check if function argument_list_expression matches with the actual one
  


def p_postfix_expression_5(p):
  '''postfix_expression : postfix_expression PERIOD ID
  | postfix_expression ARROW ID'''
  # no period in ast, but ID should always be present, making a tempNode to show 
  # ID as child of p[0].
  # TODO : This is the reduction of p1.x, where x is in ID, and postfix_expression stores p1
  # TODO : p[1].val should be defined in symbol table
  # TODO : p[3] should be a field of (get from symbol table - struct point)
  

  if (not p[1].name.startswith('Period')):
    struct_scope = find_scope(p[1].val , p[1].lno)
    if struct_scope == -1 or p[1].val not in symbol_table[struct_scope].keys():
      print("COMPILATION ERROR at line " + str(p[1].lno) + " : " + p[1].val + " not declared")

  p[0] = Node(name = 'PeriodOrArrowExpression',val = p[3],lno = p[1].lno,type = p[1].type,children = [])
  p[0].ast = build_AST(p)
  struct_name = p[1].type
  if (struct_name.endswith('*') and p[2][0] == '.') or (not struct_name.endswith('*') and p[2][0] == '->') :
    print("COMPILATION ERROR at line " + str(p[1].lno) + " : invalid operator " +  " on " + struct_name)
  if(not struct_name.startswith('struct')):
    print("COMPILATION ERROR at line " + str(p[1].lno) + ", " + p[1].val + " is not a struct")
    return

  found_scope = find_scope(struct_name , p[1].lno) 
  flag = 0 
  for curr_list in symbol_table[found_scope][struct_name]['field_list']:

    if curr_list[1] == p[3][0]:
      flag = 1 
      p[0].type = curr_list[0]
      p[0].parentStruct = struct_name
      if(len(curr_list) == 5):
        p[0].level = len(curr_list[4])
  if(p[0].level == -1):
    print("COMPILATION ERROR at line ", str(p[1].lno), ", incorrect number of dimensions specified for " + p[1].val)
 
  # if(len(p[1].parentStruct) > 0):
  #   found_scope = find_scope(p[1].parentStruct , p[1].lno)
  #   for curr_list in symbol_table[found_scope][p[1].parentStruct]['field_list']:
  #     # print(curr_list)
  #     if curr_list[1] == p[1].val:
  #       if(len(curr_list) < 5 and len(p[1].array) == 0):
  #         break
  #       if(len(curr_list) < 5 or (len(curr_list[4]) > len(p[1].array))):
  #         print("COMPILATION ERROR at line ", str(p[1].lno), ", incorrect number of dimensions for " + p[1].val)
  # else:
  #   tempScope = find_scope(p[1].val, p.lineno(1))
  #   if(len(p[1].array) > 0 and (len(p[1].parentStruct) == 0) and ('array' not in symbol_table[tempScope][p[1].val].keys() or len(symbol_table[tempScope][p[1].val]) > len(p[1].array))):
  #     print('COMPILATION ERROR at line ' + str(p[1].lno) + ' , dimensions not specified correctly for ' + p[1].val )
  #   elif(len(p[1].array) == 0 and 'array' in symbol_table[tempScope][p[1].val].keys()):
      # print('COMPILATION ERROR at line ' + str(p[1].lno) + ' , dimensions not specified correctly for ' + p[1].val )

  if flag == 0 :
    print("COMPILATION ERROR at line " + str(p[1].lno) + " : field " + " not declared in " + struct_name)
  #print("p_postfix_Expression_5 : type = ", p[0].type, " id = " , p[3])
 
  # structure things , do later



def p_postfix_expression_6(p):
  '''postfix_expression : postfix_expression INCREMENT
	| postfix_expression DECREMENT'''
  p[0] = Node(name = 'IncrementOrDecrementExpression',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [])
  p[0].ast = build_AST(p)
  found_scope = find_scope(p[1].val, p[1].lno)
  if (found_scope != -1) and ((p[1].isFunc == 1) or ('struct' in p[1].type.split())):
    print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)



#################

def p_argument_expression_list(p):
  '''argument_expression_list : assignment_expression
                              | argument_expression_list COMMA assignment_expression
  '''
  if(len(p) == 2):
    #left val empty here for now
    p[0] = Node(name = 'ArgumentExpressionList',val = '',lno = p[1].lno,type = p[1].type,children = [p[1]])
    p[0].ast = build_AST(p)
  else:
    #check if name will always be equal to ArgumentExpressionList
    # heavy doubt
    p[0] = p[1]
    p[0].children.append(p[3])
    p[0].ast = build_AST(p,[2])
  #p[0] = Node()
  # p[0] = build_AST(p)

##################


def p_unary_expression_1(p):
  '''unary_expression : postfix_expression
                      | INCREMENT unary_expression
                      | DECREMENT unary_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    #check lineno
    #also check if child should be added or not
    tempNode = Node(name = '',val = p[1],lno = p[2].lno,type = '',children = '')
    p[0] = Node(name = 'UnaryOperation',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [tempNode,p[2]])
    p[0].ast = build_AST(p)
    #Can't think of a case where this is invalid
    found_scope = find_scope(p[2].val, p[2].lno)
    if (found_scope != -1) and ((p[2].isFunc == 1) or ('struct' in p[2].type.split())):
      print("Compilation Error at line", str(p[2].lno), ":Invalid operation on", p[2].val)

def p_unary_expression_2(p):
  '''unary_expression : unary_operator cast_expression'''
  # p[1] can be &,*,+,-,~,!

  if(p[1].val == '&'):
    # no '&' child added, will deal in traversal
    p[0] = Node(name = 'AddressOfVariable',val = p[2].val,lno = p[2].lno,type = p[2].type + ' *',children = [p[2]])
    p[0].ast = build_AST(p)
  elif(p[1].val == '*'):
    if(not p[2].type.endswith('*')):
      print('COMPILATION ERROR at line ' + str(p[1].lno) + ' cannot dereference variable of type ' + p[2].type)
    p[0] = Node(name = 'PointerVariable',val = p[2].val,lno = p[2].lno,type = p[2].type[:len(p[2].type)-2],children = [p[2]])
    p[0].ast = build_AST(p)
  elif(p[1].val == '-'):
    p[0] = Node(name = 'UnaryOperationMinus',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'UnaryOperation',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [])
    p[0].ast = build_AST(p)
  # TODO: check if function can have these

def p_unary_expression_3(p):
  '''unary_expression : SIZEOF unary_expression'''
  # should I add SIZEOF in children
  p[0] = Node(name = 'SizeOf',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])
  p[0].ast = build_AST(p)

def p_unary_expression_4(p):
  '''unary_expression : SIZEOF LPAREN type_name RPAREN'''
  # should I add SIZEOF in children
  p[0] = Node(name = 'SizeOf',val = p[3].val,lno = p[3].lno,type = p[3].type,children = [p[3]])
  p[0].ast = build_AST(p,[2,4])

#########################

def p_unary_operator(p):
  '''unary_operator : AND
                    | MULTIPLY
                    | PLUS
                    | MINUS
                    | NOT
                    | LNOT
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  # p[0] = p[1]
  p[0] = Node(name = 'UnaryOperator',val = p[1],lno = p.lineno(1),type = '',children = [])
  p[0].ast = build_AST(p)

#################

def p_cast_expression(p):
  '''cast_expression : unary_expression
                     | LPAREN type_name RPAREN cast_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    # confusion about val
    p[0] = Node(name = 'TypeCasting',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [])
    p[0].ast = build_AST(p,[1,3])

################

#No type should be passed in below cases since multiplication, division, add, sub work
# for all types that are present in C.

def p_multipicative_expression(p):
  '''multiplicative_expression : cast_expression
    | multiplicative_expression MULTIPLY cast_expression
    | multiplicative_expression DIVIDE cast_expression
    | multiplicative_expression MOD cast_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    # val empty 
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'MulDiv',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')

    type_list = ['char' , 'short' , 'int' , 'long' , 'float' , 'double']
    if(p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list):
      if(p[2] is tuple):
        print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')
      else:
        print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')

    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)      
    
    if(p[2] == '%'):
      valid_type = ['char' , 'short' , 'int' , 'long']
      higher_data_type = get_higher_data_type(p[1].type , p[3].type)
      
      if higher_data_type not in valid_type:
        print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with MOD operator')

      return_data_type = higher_data_type
      if return_data_type == 'char' :
        return_data_type = 'int'
      p[0] = Node(name = 'Mod',val = p[1].val,lno = p[1].lno,type = return_data_type,children = [])
      p[0].ast = build_AST(p)

    else:
      higher_data_type = get_higher_data_type(p[1].type , p[3].type)
      return_data_type = higher_data_type
      if return_data_type == 'char' :
        return_data_type = 'int'
      p[0] = Node(name = 'MulDiv',val = p[1].val,lno = p[1].lno,type = return_data_type,children = [])
      p[0].ast = build_AST(p)

###############

def p_additive_expression(p):
  '''additive_expression : multiplicative_expression
	| additive_expression PLUS multiplicative_expression
	| additive_expression MINUS multiplicative_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'AddSub',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    elif(p[1].type.endswith('*') and not (p[3].type.endswith('*'))):
      if(p[3].type == 'float'):
        if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
        else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
      p[0] = Node(name = 'AddSub',val = '',lno = p[1].lno,type = p[1].type,children = [])
      p[0].ast = build_AST(p)
    elif(p[3].type.endswith('*') and not (p[1].type.endswith('*'))):
      if(p[1].type == 'float'):
        if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
        else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
      p[0] = Node(name = 'AddSub',val = '',lno = p[1].lno,type = p[3].type,children = [])
      p[0].ast = build_AST(p)
    elif(p[1].type.endswith('*') and p[3].type.endswith('*')):
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
      p[0] = Node(name = 'AddSub',val = '',lno = p[1].lno,type = p[1].type,children = [])
      p[0].ast = build_AST(p)
    else :
      type_list = ['char' , 'short' , 'int' , 'long' , 'float' , 'double']
      if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
        if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
        else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
      higher_data_type = get_higher_data_type(p[1].type , p[3].type)
      p[0] = Node(name = 'AddSub',val = '',lno = p[1].lno,type = higher_data_type,children = [])
      p[0].ast = build_AST(p)

    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)

##############


def p_shift_expression(p):
  '''shift_expression : additive_expression
	| shift_expression LSHIFT additive_expression
	| shift_expression RSHIFT additive_expression
	'''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'Shift',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    # We know shift only possible in int(unsigned) type, so no need to pass for now
    type_list = ['short' , 'int' , 'long']
    if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')

    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)

    higher_data_type = get_higher_data_type(p[1].type , p[3].type)
    p[0] = Node(name = 'Shift',val = '',lno = p[1].lno,type = higher_data_type,children = [])
    p[0].ast = build_AST(p)

##############

def p_relational_expression(p):
  '''relational_expression : shift_expression
	| relational_expression LESS shift_expression
	| relational_expression GREATER shift_expression
	| relational_expression LESSEQUAL shift_expression
	| relational_expression GREATEREQUAL shift_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'RelationalOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    type_list = ['char' , 'short' , 'int' , 'long' , 'float' , 'double']
    if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')

    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)

    p[0] = Node(name = 'RelationalOperation',val = '',lno = p[1].lno,type = 'int',children = [])
    p[0].ast = build_AST(p)

def p_equality_expresssion(p):
  '''equality_expression : relational_expression
	| equality_expression EQUAL relational_expression
	| equality_expression NOTEQUAL relational_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'EqualityOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    type_list = ['char' , 'short' , 'int' , 'long' , 'float' , 'double']
    if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')

    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)  

    p[0] = Node(name = 'EqualityOperation',val = '',lno = p[1].lno,type = 'int',children = [])
    p[0].ast = build_AST(p)

def p_and_expression(p):
  '''and_expression : equality_expression
	| and_expression AND equality_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'AndOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    p[0] = Node(name = 'AndOperation',val = '',lno = p[1].lno,type = '',children = [])
    p[0].ast = build_AST(p)
    valid = ['int', 'char','long','short'] #TODO: check this if more AND should be taken

    if p[1].type.split()[-1] not in valid or p[3].type.split()[-1] not in valid:
      print(p[1].lno , 'COMPILATION ERROR : Incompatible data types', p[1].type, 'and', p[3].type, 'for the AND operator')

    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)
    
    p[0].type = 'int' # should not be char, even if the and was done for two chars

# TODO: do the above expression things below as well

def p_exclusive_or_expression(p):
  '''exclusive_or_expression : and_expression
	| exclusive_or_expression XOR and_expression
	'''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'XorOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    type_list = ['char' , 'short' , 'int' , 'long']
    if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)

    p[0] = Node(name = 'XorOperation',val = '',lno = p[1].lno,type = 'int',children = [])
    p[0].ast = build_AST(p)

def p_inclusive_or_expression(p):
  '''inclusive_or_expression : exclusive_or_expression
	| inclusive_or_expression OR exclusive_or_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'OrOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    type_list = ['char' , 'short' , 'int' , 'long']
    if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
    
    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)
    p[0] = Node(name = 'OrOperation',val = '',lno = p[1].lno,type = 'int',children = [])
    p[0].ast = build_AST(p)

def p_logical_and_expression(p):
  '''logical_and_expression : inclusive_or_expression 
  | logical_and_expression LAND inclusive_or_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'LogicalAndOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    type_list = ['char' , 'short' , 'int' , 'long','float','double']
    if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')

    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)
    p[0] = Node(name = 'LogicalAndOperation',val = '',lno = p[1].lno,type = 'int',children = [])
    p[0].ast = build_AST(p)

def p_logical_or_expression(p):
  '''logical_or_expression : logical_and_expression
	| logical_or_expression LOR logical_and_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'LogicalOrOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    type_list = ['char' , 'short' , 'int' , 'long','float','double']
    if p[1].type.split()[-1] not in type_list or p[3].type.split()[-1] not in type_list:
      if(p[2] is tuple):
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2][0] +  ' operator')  
      else:
          print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')


    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and (p[1].isFunc == 1):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and (p[3].isFunc == 1):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)
    p[0] = Node(name = 'LogicalOrOperation',val = '',lno = p[1].lno,type = 'int',children = [])
    p[0].ast = build_AST(p)

# TODO: everything for conditional_expression
def p_conditional_expression(p):
  '''conditional_expression : logical_or_expression
	| logical_or_expression CONDOP expression COLON conditional_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    
    p[0] = Node(name = 'ConditionalOperation',val = '',lno = p[1].lno,type = '',children = [])
    p[0].ast = build_AST(p)


def p_assignment_expression(p):
  '''assignment_expression : conditional_expression 
                           | unary_expression assignment_operator assignment_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    # print(p[1].type, p[3].type)
    if(p[1].type == '' or p[3].type == ''):
      p[0] = Node(name = 'AssignmentOperation',val = '',lno = p[1].lno,type = 'int',children = [])
      p[0].ast = build_AST(p)
      return
    if p[1].type == '-1' or p[3].type == '-1':
      return
    if('const' in p[1].type.split()):
      print('Error, modifying a variable declared with const keyword at line ' + str(p[1].lno))
    if('struct' in p[1].type.split() and 'struct' not in p[3].type.split()):
      print('COMPILATION ERROR at line ' + str(p[1].lno) + ', cannot assign variable of type ' + p[3].type + ' to ' + p[1].type)
    elif('struct' not in p[1].type.split() and 'struct' in p[3].type.split()):
      print('COMPILATION ERROR at line ' + str(p[1].lno) + ', cannot assign variable of type ' + p[3].type + ' to ' + p[1].type)
    elif(p[1].type.split()[-1] != p[3].type.split()[-1]):
      print('Warning at line ' + str(p[1].lno) + ': type mismatch in assignment')
    tempScope = find_scope(p[1].val, p.lineno(1))
    # if(len(p[1].array) > 0 and (len(p[1].parentStruct) == 0) and ('array' not in symbol_table[tempScope][p[1].val].keys() or len(symbol_table[tempScope][p[1].val]) > len(p[1].array))):
    #   print('COMPILATION ERROR at line ' + str(p[1].lno) + ' , dimensions not specified correctly for ' + p[1].val )
    # elif(len(p[1].array) == 0 and (len(p[1].parentStruct) == 0) and 'array' in symbol_table[tempScope][p[1].val].keys()):
    #   print('COMPILATION ERROR at line ' + str(p[1].lno) + ' , dimensions not specified correctly for ' + p[1].val )
    if(p[1].level != p[3].level):
      print("COMPILATION ERROR at line ", str(p[1].lno), ", type mismatch in assignment")
    if(p[1].level != 0 or p[3].level != 0):
      print("COMPILATION ERROR at line ", str(p[1].lno), ", cannot assign array pointer")
    if(len(p[1].parentStruct) > 0):
      found_scope = find_scope(p[1].parentStruct , p[1].lno)
      for curr_list in symbol_table[found_scope][p[1].parentStruct]['field_list']:
        # print(curr_list)
        if curr_list[1] == p[1].val:
          if(len(curr_list) < 5 and len(p[1].array) == 0):
            break
          if(len(curr_list) < 5 or (len(curr_list[4]) < len(p[1].array))):
            print("COMPILATION ERROR at line ", str(p[1].lno), ", incorrect number of dimensions")
    found_scope = find_scope(p[1].val, p[1].lno)
    if (found_scope != -1) and ((p[1].isFunc == 1)):
      print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)

    found_scope = find_scope(p[3].val, p[3].lno)
    if (found_scope != -1) and ((p[3].isFunc == 1)):
      print("Compilation Error at line", str(p[3].lno), ":Invalid operation on", p[3].val)

    if p[2].val != '=':
      if ('struct' in p[1].type.split()) or ('struct' in p[3].type.split()):
        print("Compilation Error at line", str(p[1].lno), ":Invalid operation on", p[1].val)
    
    p[0] = Node(name = 'AssignmentOperation',val = '',type = p[1].type, lno = p[1].lno, children = [], level = p[1].level)
    p[0].ast = build_AST(p)

def p_assignment_operator(p):
  '''assignment_operator : EQUALS
	| MULTIPLYEQUAL
	| DIVIDEEQUAL
	| MODEQUAL
	| PLUSEQUAL
	| MINUSEQUAL
	| LSHIFTEQUAL
	| RSHIFTEQUAL
	| ANDEQUAL
	| XOREQUAL
	| OREQUAL
	'''
  #p[0] = Node()
  # p[0] = build_AST(p)
  # p[0] = p[1]
  p[0] = Node(name = 'AssignmentOperator',val = p[1],type = '', lno = p.lineno(1), children = [p[1]])
  p[0].ast = build_AST(p)

def p_expression(p):
  '''expression : assignment_expression
	| expression COMMA assignment_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    # optimized here, might also be possible above somewhere
    p[0] = p[1]
    p[0].children.append(p[3])
    p[0].ast = build_AST(p,[2])

def p_constant_expression(p):
  '''constant_expression : conditional_expression'''
  # p[0] = build_AST(p)
  p[0] = p[1]
  p[0].ast = build_AST(p)

def p_declaration(p):
  '''declaration : declaration_specifiers SEMICOLON
	| declaration_specifiers init_declarator_list SEMICOLON
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  # global typedef_list
  # global all_typedef
  if(len(p) == 3):
    p[0] = p[1]
    p[0].ast = build_AST(p,[2])
  else:
    # a = 1
    p[0] = Node(name = 'Declaration',val = p[1],type = p[1].type, lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p,[3])
    flag = 1
    if('void' in p[1].type.split()):
      flag = 0
    for child in p[2].children:

      if(child.name == 'InitDeclarator'):
        if(p[1].type.startswith('typedef')):
          print("COMPILATION ERROR at line " + str(p[1].lno) + ": typedef intialized")
          continue
        if(child.children[0].val in symbol_table[currentScope].keys()):
          print(p.lineno(1), 'COMPILATION ERROR : ' + child.children[0].val + ' already declared')
        # print(child.children[0].val,child.children[1].val)
        symbol_table[currentScope][child.children[0].val] = {}
        symbol_table[currentScope][child.children[0].val]['type'] = p[1].type
        symbol_table[currentScope][child.children[0].val]['value'] = child.children[1].val
        symbol_table[currentScope][child.children[0].val]['size'] = get_data_type_size(p[1].type)
        totalEle = 1
        if(len(child.children[0].array) > 0):
          symbol_table[currentScope][child.children[0].val]['array'] = child.children[0].array
          for i in child.children[0].array:
            totalEle = totalEle*i
        if(len(child.children[0].type) > 0):
          symbol_table[currentScope][child.children[0].val]['type'] = p[1].type + ' ' + child.children[0].type 
          symbol_table[currentScope][child.children[0].val]['size'] = 8
        elif(flag == 0):
          print("COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.children[0].val + " cannot have type void")
        symbol_table[currentScope][child.children[0].val]['size'] *= totalEle
      else:
        # print(p[1].type)
        # print("here : ", child.val)
        # if(p[1].type.startswith('typedef')):
        #   to_be_typedef = []
        #   for i in p[1].type.split():
        #     if(i != 'typedef'):
        #       to_be_typedef.append(i)
        #   # print(to_be_typedef)
        #   for i in child.type:
        #     to_be_typedef.append(i)
        #   to_be_typedef_str = ' '.join([str(elem) for elem in to_be_typedef])
        #   if(to_be_typedef_str not in typedef_list.keys()):
        #     typedef_list[to_be_typedef_str] = [child.val]
        #     all_typedef.append(child.val)
        #   else:
        #     typedef_list[to_be_typedef_str].append(child.val)
        #     all_typedef.append(child.val)
        if(child.val in symbol_table[currentScope].keys()):
          print(p.lineno(1), 'COMPILATION ERROR : ' + child.val + ' already declared')
        symbol_table[currentScope][child.val] = {}
        symbol_table[currentScope][child.val]['type'] = p[1].type
        # print(p[1].type)
        symbol_table[currentScope][child.val]['size'] = get_data_type_size(p[1].type)
        totalEle = 1
        if(len(child.array) > 0):
          symbol_table[currentScope][child.val]['array'] = child.array
          for i in child.array:
            totalEle = totalEle*i
        if(len(child.type) > 0):
          symbol_table[currentScope][child.val]['type'] = p[1].type + ' ' + child.type
          symbol_table[currentScope][child.val]['size'] = 8
        elif(flag == 0):
          print("COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.val + " cannot have type void")
        symbol_table[currentScope][child.val]['size'] *= totalEle
        # TODO : Confirm with others about two possible approaches
        # if(p[1].type.startswith('struct')):
        #   found_scope = find_if_ID_is_declared(p[1].type, p.lineno(1))
        #   if found_scope != -1:
        #     symbol_table[currentScope][child.val]['field_list'] = symbol_table[found_scope][p[1].type]['field_list']

        
        
        

# TODO : change the below to support long, short etc.
def p_declaration_specifiers(p):
  '''declaration_specifiers : storage_class_specifier
	| storage_class_specifier declaration_specifiers
	| type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
  '''
  # TypeQualifier, TypeSpecifier1, StorageClassSpecifier
  if(len(p) == 2):
    p[0] = p[1]
    p[0].ast = build_AST(p)
    # global curFuncReturnType
    curType.append(p[1].type)
    # print('here',curType[-1],curFuncReturnType)
  elif(len(p) == 3):
    if(p[1].name == 'StorageClassSpecifier' and p[2].name.startswith('StorageClassSpecifier')):
      print("Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type)
    if(p[1].name == 'TypeSpecifier1' and (p[2].name.startswith('TypeSpecifier1') or p[2].name.startswith('StorageClassSpecifier') or p[2].name.startswith('TypeQualifier'))):
      print("Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type)
    if(p[1].name == 'TypeQualifier' and (p[2].name.startswith('StorageClassSpecifier') or p[2].name.startswith('TypeQualifier'))):
      print("Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type)
    # if(p[1].name == '')
    curType.pop()
    curType.append(p[1].type + ' ' + p[2].type)
    
    ty = ""
    if len(p[1].type) > 0:
      ty = p[1].type + ' ' + p[2].type
    else:
      ty = p[2].type
    curType.append(ty)
    # print(ty)
    p[0] = Node(name = p[1].name + p[2].name,val = p[1],type = ty, lno = p[1].lno, children = [])
    p[0].ast = build_AST(p)
  #p[0] = Node()
  # p[0] = build_AST(p)




def p_init_declarator_list(p):
  '''init_declarator_list : init_declarator
	| init_declarator_list COMMA init_declarator
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = Node(name = 'InitDeclaratorList', val = '', type = '', lno = p.lineno(1), children = [p[1]])
    p[0].ast = build_AST(p)
  else:
    #check onceƒ
    p[0] = p[1]
    p[0].children.append(p[3])
    p[0].ast = build_AST(p,[2])

def p_init_declarator(p):
  '''init_declarator : declarator
	| declarator EQUALS initializer
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    # extra node might be needed for error checking
    #maybe make different function to do this
    p[0] = p[1]
    p[0].ast = build_AST(p)
  else:
    # tempNode = Node(name = '',val = p[2],type = '', lno = p[1].lno, children = [])
    # print("here" + p[1].type)
    # if(p[1].type.startswith('typedef')):
    #   print("COMPILATION ERROR at line " + str(p[1].lno) + " typedef intialized")
    p[0] = Node(name = 'InitDeclarator',val = '',type = p[1].type,lno = p.lineno(1), children = [p[1],p[3]], array = p[1].array)
    p[0].ast = build_AST(p)
    if(len(p[1].array) > 0 and (p[3].maxDepth == 0 or p[3].maxDepth > len(p[1].array))):
      print('COMPILATION ERROR at line ' + str(p.lineno(1)) + ' , invalid initializer')
    if(p[1].level != p[3].level):
      print("COMPILATION ERROR at line ", str(p[1].lno), ", type mismatch")

def p_storage_class_specifier(p):
  '''storage_class_specifier : TYPEDEF
	| EXTERN
	| STATIC
	| AUTO
	| REGISTER
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  # p[0] = p[1]
  p[0] = Node(name = 'StorageClassSpecifier',val = '',type = p[1], lno = p.lineno(1), children = [])
  # p[0].ast = build_AST(p)


def p_type_specifier_1(p):
  '''type_specifier : VOID
                    | CHAR
                    | SHORT
                    | INT
                    | LONG
                    | FLOAT
                    | DOUBLE
                    | SIGNED
                    | UNSIGNED
                    | TYPE_NAME
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  p[0] = Node(name = 'TypeSpecifier1',val = '',type = p[1], lno = p.lineno(1), children = [])
  # p[0].ast = build_AST(p)

def p_type_specifier_2(p):
  '''type_specifier : struct_or_union_specifier
                    | enum_specifier '''
  p[0] = p[1]
  p[0].ast = build_AST(p)
  # p[0] = Node(name = '',val = '',type = p[1], lno = p.lineno(1), children = [])

def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier : struct_or_union ID openbrace struct_declaration_list closebrace
  | struct_or_union openbrace struct_declaration_list closebrace
  | struct_or_union ID
  '''
  # p[0] = build_AST(p)
  # TODO : check the semicolon thing after closebrace in gramamar
  # TODO : Manage the size and offset of fields
  p[0] = Node(name = 'StructOrUnionSpecifier', val = '', type = '', lno = p[1].lno , children = [])
  if len(p) == 6:
    val_name = p[1].type + ' ' + p[2]
    p[0].ast = build_AST(p,[3,5])
    if val_name in symbol_table[currentScope].keys():
      print('COMPILATION ERROR : near line ' + str(p[1].lno) + ' struct already declared')
    valptr_name = val_name + ' *'
    symbol_table[currentScope][val_name] = {}
    symbol_table[currentScope][val_name]['type'] = val_name
    symbol_table[currentScope][valptr_name] = {}
    symbol_table[currentScope][valptr_name]['type'] = valptr_name
    temp_list = []
    curr_offset = 0 
    max_size = 0
    for child in p[4].children:
      for prev_list in temp_list:
        if prev_list[1] == child.val:
          print('COMPILATION ERROR : line ' + str(p[4].lno) + ' : ' + child.val + ' already deaclared')
      if get_data_type_size(child.type) == -1:
        print("COMPILATION ERROR at line " + str(child.lno) + " : data type not defined")
      SZ = get_data_type_size(child.type)
      curr_list = [child.type, child.val, SZ, curr_offset]
      totalEle = 1
      if(len(child.array) > 0):
        curr_list.append(child.array)
        for ele in child.array:
          totalEle *= ele
      curr_offset = curr_offset + get_data_type_size(child.type)*totalEle
      curr_list[2] *= totalEle
      SZ *= totalEle
      max_size = max(max_size , SZ)
      if p[1].type == 'union':
        curr_list[3] = 0
      temp_list.append(curr_list)

    if p[1].type == 'union':
      curr_offset = max_size
    symbol_table[currentScope][val_name]['field_list'] = temp_list
    symbol_table[currentScope][val_name]['size'] = curr_offset
    symbol_table[currentScope][valptr_name]['field_list'] = temp_list
    symbol_table[currentScope][valptr_name]['size'] = 8

  elif len(p) == 3:
    p[0].type = p[1].type + ' ' + p[2]
    p[0].ast = build_AST(p)
    found_scope = find_scope(p[0].type, p[1].lno)
    if(found_scope == -1):
      print("COMPILATION ERROR : at line " + str(p[1].lno) + ", " + p[0].type + " is not a type")
  else:
    p[0].ast = build_AST(p,[2,4])


def p_struct_or_union(p):
  '''struct_or_union : STRUCT
	| UNION
  '''

  # p[0] = build_AST(p)
  # print(p[1])
  if p[1] == 'struct':
    p[0] = Node(name = 'StructOrUNion', val = '', type = 'struct', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'StructOrUNion', val = '', type = 'union', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)

def p_struct_declaration_list(p):
  '''struct_declaration_list : struct_declaration
	| struct_declaration_list struct_declaration
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'StructDeclarationList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p)
  if(len(p) == 2):
    p[0].children = p[1].children
  else:
    p[0].children = p[1].children
    p[0].children.extend(p[2].children)


def p_struct_declaration(p):
  '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'StructDeclaration', val = '', type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p,[3])
  p[0].children = p[2].children
  for child in p[0].children:
    if len(child.type) > 0:
      child.type = p[1].type + ' ' + child.type
    else:
      if('void' in p[1].type.split()):
        print("COMPILATION ERROR at line " + str(p[1].lno) + ", variable " + child.val + " cannot have type void")
      child.type = p[1].type
  

def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list : type_specifier specifier_qualifier_list
  | type_specifier
  | type_qualifier specifier_qualifier_list
  | type_qualifier
  '''
  #p[0] = Node()
  #p[0] = build_AST(p)
  p[0] = Node(name = 'SpecifierQualifierList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p)

def p_struct_declarator_list(p):
  '''struct_declarator_list : struct_declarator
	| struct_declarator_list COMMA struct_declarator
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'StructDeclaratorList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  # print(p[1].type)
  if(len(p) == 2):
    p[0].children.append(p[1])
    p[0].ast = build_AST(p)
  else:
    p[0].children = p[1].children 
    p[0].children.append(p[3])
    p[0].ast = build_AST(p,[2])
    # print(p[3].type)

def p_struct_declarator(p):  
  '''struct_declarator : declarator
	| COLON constant_expression
	| declarator COLON constant_expression
  '''
  #p[0] = build_AST(p)
  if len(p) == 2 or len(p) == 4:
    p[0] = p[1] 
    p[0].ast = build_AST(p)
  if len(p) == 3:
    p[0] = p[2]
    p[0].ast = build_AST(p)
  

def p_enum_specifier(p):
  '''enum_specifier : ENUM openbrace enumerator_list closebrace
	| ENUM ID openbrace enumerator_list closebrace
	| ENUM ID
  '''
  #p[0] = build_AST(p)
  if(len(p) == 5):
    p[0] = Node(name = 'EnumSpecifier', val = '', type = 'Enum_Specifier', lno = p[3].lno, children = [])
    p[0].ast = build_AST(p)
  elif(len(p) == 6):
    p[0] = Node(name = 'EnumSpecifier', val = '', type = 'Enum_Specifier', lno = p[4].lno, children = [])
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'EnumSpecifier', val = '', type = 'Enum_Specifier', lno = p[2].lno, children = [])
    p[0].ast = build_AST(p)

def p_enumerator_list(p):
  '''enumerator_list : enumerator
	| enumerator_list COMMA enumerator
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'EnumeratorList', val= '', type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p)
  if(len(p) == 2):
    p[0].children.append(p[1])
  else:
    p[0].children.append(p[3])

def p_enumerator(p):
  '''enumerator : ID
	| ID EQUALS constant_expression
	'''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'Enumerator', val = '', type = '', lno = p.lineno(1), children = [])
  p[0].ast = build_AST(p)

def p_type_qualifier(p):
    '''type_qualifier : CONST
                      | VOLATILE
    '''
    p[0] = Node(name = 'TypeQualifier', val = '', type = p[1], lno = p.lineno(1), children = [])
    #p[0] = build_AST(p)

def p_declarator(p):
  '''declarator : pointer direct_declarator
  | direct_declarator
  '''
  global curFuncReturnType
  # print(p[1].children)
  # p[0] = Node(name = 'Declarator', val = '', type = '', lno = p.lineno(1), children = [])
  if(len(p) == 2):
    p[0] = p[1]
    p[0].name = 'Declarator'
    p[0].val = p[1].val
    p[0].array = p[1].array
    p[0].ast = build_AST(p)
  else:
    p[0] = p[2]
    p[0].name = 'Declarator'
    p[0].type = p[1].type
    p[0].ast = build_AST(p)
    # print(p[1].type)
    if(p[2].val in symbol_table[parent[currentScope]] and 'isFunc' in symbol_table[parent[currentScope]][p[2].val].keys()):
      symbol_table[parent[currentScope]][p[2].val]['type'] = symbol_table[parent[currentScope]][p[2].val]['type'] + ' ' + p[1].type
      curFuncReturnType = curFuncReturnType + ' ' + p[1].type
      # print(symbol_table[parent[currentScope]][p[2].val]['type'])
    p[0].val = p[2].val
    p[0].array = p[2].array
  # print(p[0].children)
  # if(p[1].name == 'ID'):
  #     p[0].name = 'ID'

def p_direct_declarator_1(p):
  '''direct_declarator : ID
                        | LPAREN declarator RPAREN
                        | direct_declarator lopenparen parameter_type_list RPAREN
                        | direct_declarator lopenparen identifier_list RPAREN
  ''' 
  # 
  global curFuncReturnType
  if(len(p) == 2):
    # curScopeName = 3
    # find_if_ID_is_declared(p[1],p.lineno(1))
    p[0] = Node(name = 'ID', val = p[1], type = '', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)
    # p[0].val = p[1]
    # # insert in symbol table here
    # if(p[1] in symbol_table[currentScope].keys()):
    #   print( 'COMPILATION ERROR at line : ' + p.lineno(1) + ", " + p[1] + ' already declared')

  elif(len(p) == 4):
    p[0] = p[2]
    p[0].ast = build_AST(p,[1,3])
  else:
    p[0] = p[1]
    p[0].ast = build_AST(p,[2,4])
    p[0].children = p
  if(len (p) == 5 and p[3].name == 'ParameterList'):
    p[0].children = p[3].children
    p[0].type = curType[-1]
    # print(p[0].type)
    # print(p[0].children)
    if(p[1].val in symbol_table[parent[currentScope]].keys()):
      print('COMPILATION ERROR : near line ' + str(p[1].lno) + ' function already declared')
    symbol_table[parent[currentScope]][p[1].val] = {}
    
    symbol_table[parent[currentScope]][p[1].val]['isFunc'] = 1
    tempList = []
    for child in p[3].children:
      # print(child.type)
      tempList.append(child.type)
    symbol_table[parent[currentScope]][p[1].val]['argumentList'] = tempList
    symbol_table[parent[currentScope]][p[1].val]['type'] = curType[-1-len(tempList)]
    curFuncReturnType = copy.deepcopy(curType[-1-len(tempList)])
    # symbol_table[parent[currentScope]][p[1].val]['FunctionScope'] = currentScope
  #p[0] = build_AST(p)

def p_direct_declarator_2(p):
  '''direct_declarator : direct_declarator LSQUAREBRACKET INT_CONST RSQUAREBRACKET'''
  p[0] = Node(name = 'ArrayDeclarator', val = p[1].val, type = '', lno = p.lineno(1),  children = [])
  p[0].ast = build_AST(p)
  p[0].array = copy.deepcopy(p[1].array)
  p[0].array.append(int(p[3][0]))

def p_direct_declarator_3(p):
  '''direct_declarator : direct_declarator LSQUAREBRACKET RSQUAREBRACKET
                        | direct_declarator lopenparen RPAREN'''
  p[0] = p[1]
  if(p[3] == ')'):
    p[0].ast = build_AST(p,[2,3])
  else:
    p[0].ast = build_AST(p)  
  global curFuncReturnType
  if(p[3] == ')'):
    # p[0].type = curType[-1]
    # print(p[0].type)
    if(p[1].val in symbol_table[parent[currentScope]].keys()):
      print('COMPILATION ERROR : near line ' + str(p[1].lno) + ' function already declared')
    symbol_table[parent[currentScope]][p[1].val] = {}
    symbol_table[parent[currentScope]][p[1].val]['type'] = curType[-1]
    curFuncReturnType = copy.deepcopy(curType[-1])
    symbol_table[parent[currentScope]][p[1].val]['isFunc'] = 1
    symbol_table[parent[currentScope]][p[1].val]['argumentList'] = []
    # symbol_table[parent[currentScope]][p[1].val]['type'] = curType[-1-len(tempList)]
    # curFuncReturnType = copy.deepcopy(curType[-1])
    # if(len(p[3].children) > 0):
    #   tempList = []
    # for child in p[3].children:
    #   # print(child.type)
    #   tempList.append(child.type)
    # symbol_table[currentScope][p[1].val]['argumentList'] = tempList

def p_pointer(p):
  '''pointer : MULTIPLY 
              | MULTIPLY type_qualifier_list
              | MULTIPLY pointer
              | MULTIPLY type_qualifier_list pointer
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = Node(name = 'Pointer',val = '',type = '*', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)
  elif(len(p) == 3):
    p[0] = Node(name = 'Pointer',val = '',type = p[2].type + ' *', lno = p.lineno(1), children = [])
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'Pointer',val = '',type = p[2].type + ' *', lno = p[2].lno, children = [])
    p[0].ast = build_AST(p)

def p_type_qualifier_list(p):
  '''type_qualifier_list : type_qualifier
                        | type_qualifier_list type_qualifier
  '''
  #p[0] = Node()
  if(len(p) == 2):
    p[0] = p[1]
    p[0].name = 'TypeQualifierList'
    p[0].children = p[1]
    p[0].ast = build_AST(p)
  else:
    p[0] = p[1]
    p[0].children.append(p[2])
    p[0].type = p[1].type + " " + p[2].type
    p[0].name = 'TypeQualifierList'
    p[0].ast = build_AST(p)
    # p[0] = Node(name = '',val = '',type = '', lno = p[1].lno, children = [])

def p_parameter_type_list(p):
  '''parameter_type_list : parameter_list
                          | parameter_list COMMA ELLIPSIS
  '''
  #p[0] = Node()
  p[0] = p[1]
  p[0].ast = build_AST(p)
  # TODO : see what to do in case of ellipsis

def p_parameter_list(p):
    '''parameter_list : parameter_declaration
                      | parameter_list COMMA parameter_declaration
    '''
    #p[0] = Node()
    p[0] = Node(name = 'ParameterList', val = '', type = '', children = [], lno = p.lineno(1))
    if(len(p) == 2):
      p[0].ast = build_AST(p)
      p[0].children.append(p[1])
    else:
      p[0].ast = build_AST(p,[2])
      p[0].children = p[1].children
      p[0].children.append(p[3])

def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator
                             | declaration_specifiers abstract_declarator
                             | declaration_specifiers
    '''
    #p[0] = Node()
    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
      p[0].name = 'ParameterDeclaration'
    else:
      p[0] = Node(name = 'ParameterDeclaration',val = p[2].val,type = p[1].type, lno = p[1].lno, children = [])
      p[0].ast = build_AST(p)
      if(len(p[2].type) > 0):
        p[0].type = p[1].type + ' ' + p[2].type
    if(p[2].name == 'Declarator'):
      if(p[2].val in symbol_table[currentScope].keys()):
        print(p.lineno(1), 'COMPILATION ERROR : ' + p[2].val + ' parameter already declared')
      symbol_table[currentScope][p[2].val] = {}
      symbol_table[currentScope][p[2].val]['type'] = p[1].type
      
      if(len(p[2].type) > 0):
        symbol_table[currentScope][p[2].val]['type'] = p[1].type + ' ' + p[2].type
        symbol_table[currentScope][p[2].val]['size'] = get_data_type_size(p[1].type+ ' ' + p[2].type)
      else:
        if('void' in p[1].type.split()):
          print("COMPILATION ERROR at line " + str(p[1].lno) + ", parameter " + p[2].val + " cannot have type void")
        symbol_table[currentScope][p[2].val]['size'] = get_data_type_size(p[1].type)
      if(len(p[2].array) > 0):
        symbol_table[currentScope][p[2].val]['array'] = p[2].array


def p_identifier_list(p):
    '''identifier_list : ID
                       | identifier_list COMMA ID
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 2):
      p[0] = Node(name = 'IdentifierList',val = p[1],type = '', lno = p.lineno(1), children = [p[1]])
      p[0].ast = build_AST(p)
    else:
      p[0] = p[1]
      p[0].children.append(p[3])
      p[0].name = 'IdentifierList'
      p[0].ast = build_AST(p,[2])

def p_type_name(p):
    '''type_name : specifier_qualifier_list
                 | specifier_qualifier_list abstract_declarator
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 2):
      p[0] = p[1]
      p[0].name = 'TypeName'
      p[0].ast = build_AST(p)
    else:
      p[0] = Node(name = 'TypeName',val = '',type = p[1].type, lno = p[1].lno, children = [])
      p[0].ast = build_AST(p)

def p_abstract_declarator(p):
    '''abstract_declarator : pointer 
                           | direct_abstract_declarator
                           | pointer direct_abstract_declarator
    '''
    #p[0] = Node()
    if(len(p) == 2):
      p[0] = p[1]
      p[0].name = 'AbstractDeclarator'
      p[0].ast = build_AST(p)
    elif(len(p) == 3):
      p[0] = Node(name = 'AbstractDeclarator',val = p[2].val,type = p[1].type + ' *', lno = p[1].lno, children = [])
      p[0].ast = build_AST(p)

def p_direct_abstract_declarator_1(p):
    '''direct_abstract_declarator : LPAREN abstract_declarator RPAREN
                                  | LSQUAREBRACKET RSQUAREBRACKET
                                  | LSQUAREBRACKET constant_expression RSQUAREBRACKET
                                  | direct_abstract_declarator LPAREN constant_expression RPAREN 
                                  | LPAREN RPAREN
                                  | LPAREN parameter_type_list RPAREN
                                  | direct_abstract_declarator LPAREN parameter_type_list RPAREN
    '''
    #p[0] = Node()
    if(len(p) == 3):
      p[0] = Node(name = 'DirectAbstractDeclarator1',val = '',type = '', lno = p.lineno(1), children = [])
      # p[0].ast = build_AST(p)
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'DirectAbstractDeclarator1'
      p[0].ast = build_AST(p,[1,3])
      # if(p[1] == '('):
      #   p[0].ast = build_AST(p,[1,3])
      # else:
      #   p[0].ast = build_AST(p)
    else:
      p[0] = Node(name = 'DirectAbstractDeclarator1',val = p[1].val,type = p[1].val, lno = p[1].lno, children = [p[3]])
      p[0].ast = build_AST(p,[2,4])
      # if(p[2] == '('):
      #   p[0].ast = build_AST(p)
      # else:
      #   p[0].ast = build_AST(p)

def p_direct_abstract_declarator_2(p):
  '''direct_abstract_declarator : direct_abstract_declarator LPAREN RPAREN'''
  p[0] = Node(name = 'DirectAbstractDEclarator2', val = p[1].val, type = p[1].type, lno = p[1].lno, children = [])
  p[0].ast = build_AST(p,[2,3])

def p_initializer(p):
    '''initializer : assignment_expression
                   | openbrace initializer_list closebrace
                   | openbrace initializer_list COMMA closebrace                                   
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
    else:
      p[0] = p[2]
    p[0].name = 'Initializer'
    if(len(p) == 4):
      p[0].maxDepth = p[2].maxDepth + 1
      p[0].ast = build_AST(p,[1,3])
    elif(len(p) == 5):
      p[0].ast = build_AST(p,[1,3,4])

def p_initializer_list(p):
  '''initializer_list : initializer
  | initializer_list COMMA initializer
  '''
  #p[0] = Node()
  if(len(p) == 2):
    p[0] = Node(name = 'InitializerList', val = '', type = '', children = [p[1]], lno = p.lineno(1), maxDepth = p[1].maxDepth)
    p[0].ast = build_AST(p)
  else:
    p[0] = Node(name = 'InitializerList', val = '', type = '', children = [], lno = p.lineno(1))
    p[0].ast = build_AST(p,[2])
    if(p[1].name != 'InitializerList'):
      p[0].children.append(p[1])
    else:
      p[0].children = p[1].children
    p[0].children.append(p[3])
    p[0].maxDepth = max(p[1].maxDepth, p[3].maxDepth)

def p_statement(p):
    '''statement : labeled_statement
                 | compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
    '''
    # p[0] = p[1]
    p[0] = Node(name = 'Statement', val = '', type ='', children = [], lno = p.lineno(1))
    p[0].ast = build_AST(p)
    # print('here', p[0])
def p_labeled_statement_1(p):
    '''labeled_statement : ID COLON statement '''
    p[0] = Node(name = 'LabeledStatement', val = '', type ='', children = [], lno = p.lineno(1) )
    p[0].ast = build_AST(p,[2])

def p_labeled_statement_2(p):
    '''labeled_statement : CASE constant_expression COLON statement'''
    p[0] = Node(name = 'CaseStatement', val = '', type = '', children = [], lno = p.lineno(1))
    p[0].ast = build_AST(p)

def p_labeled_statement_3(p):
    '''labeled_statement : DEFAULT COLON statement'''
    p[0] = Node(name = 'DefaultStatement', val = '', type = '', children = [], lno = p.lineno(1))
    p[0].ast = build_AST(p)

def p_compound_statement(p):
    '''compound_statement : openbrace closebrace
                          | openbrace statement_list closebrace
                          | openbrace declaration_list closebrace
                          | openbrace declaration_list statement_list closebrace
    '''  
    #p[0] = Node()
    #TODO : see what to do in in first case
    if(len(p) == 3):
      p[0] = Node(name = 'CompoundStatement',val = '',type = '', lno = p.lineno(1), children = [])
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'CompoundStatement'
      p[0].ast = build_AST(p,[1,3])
    elif(len(p) == 4):
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,4])
    else:
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,5])

def p_function_compound_statement(p):
    '''function_compound_statement : LCURLYBRACKET closebrace
                          | LCURLYBRACKET statement_list closebrace
                          | LCURLYBRACKET declaration_list closebrace
                          | LCURLYBRACKET declaration_list statement_list closebrace
    '''  
    #p[0] = Node()
    if(len(p) == 3):
      p[0] = Node(name = 'CompoundStatement',val = '',type = '', lno = p.lineno(1), children = [])
      # p[0].ast = build_AST(p,[1,3])
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'CompoundStatement'
      p[0].ast = build_AST(p)
      # print('building')
    elif(len(p) == 4):
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,4])
    else:
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p,[1,5])


def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration
    '''
    #p[0] = Node()
    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
    else:
      p[0] = Node(name = 'DeclarationList', val = '', type = '', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p)
      if(p[1].name != 'DeclarationList'):
        p[0].children.append(p[1])
      else:
        p[0].children = p[1].children
      p[0].children.append(p[2])

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement
    '''
    #p[0] = Node()
    if(len(p) == 2):
      p[0] = p[1]
      p[0].ast = build_AST(p)
      print('here',p[0])
      # p[0].name = 'StatementList'
    else:
      p[0] = Node(name = 'StatementList', val='', type='', children = [], lno = p.lineno(1))
      p[0].ast = build_AST(p)
      # print(p[2].lno)
      # if(p[1] is None):
      #   print('yes')
      if(p[1].name != 'StatmentList'):
        p[0].children.append(p[1])
      else:
        p[0].children = p[1].children
      p[0].children.append(p[2])

def p_expression_statement(p):
    '''expression_statement : SEMICOLON
                            | expression SEMICOLON
    '''
    # p[0] = Node()
    p[0] = Node(name = 'ExpressionStatement', val='', type='', children = [], lno = p.lineno(1))
    # print(p[])
    # print(p[0],'here2')
    if(len(p) == 3):
      p[0].ast = build_AST(p,[2])
      p[0].val = p[1].val
      p[0].type = p[1].type
      p[0].children = p[1].children
    p[0].name = 'ExpressionStatement'
    # TODO : see what to do in case of only semicolon in rhs
    # else:
    #   p[0] = Node(name = '',val = '',type = p[1], lno = p.lineno(1), children = [])
    

def p_selection_statement_1(p):
    '''selection_statement : if LPAREN expression RPAREN statement %prec IFX'''
    #p[0] = Node()
    p[0] = Node(name = 'IfStatment', val = '', type = '', children = [], lno = p.lineno(1))
    p[0].ast = build_AST(p,[2,4])
  
def p_selection_statement_2(p):
    '''selection_statement : if LPAREN expression RPAREN statement ELSE statement'''
    p[0] = Node(name = 'IfElseStatement', val = '', type = '', children = [], lno = p.lineno(1))
    p[0].ast = build_AST(p,[2,4])

def p_if(p):
  '''if : IF'''
  p[0] = p[1]
  p[0] = build_AST(p)

def p_selection_statement_3(p):
    '''selection_statement : switch LPAREN expression RPAREN statement'''
    p[0] = Node(name = 'SwitchStatement', val = '', type = '', children = [], lno = p.lineno(1))
    global switchDepth
    switchDepth -= 1
    p[0].ast = build_AST(p,[2,4])

def p_switch(p):
  '''switch : SWITCH'''
  p[0] = p[1]
  global switchDepth
  switchDepth += 1
  p[0] = build_AST(p)

# remember : here statement added in grammar
def p_iteration_statement_1(p):
    '''iteration_statement : while LPAREN expression RPAREN statement'''
    #p[0] = Node()
    p[0] = Node(name = 'WhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
    global loopingDepth
    loopingDepth -= 1
    p[0] = build_AST(p,[2,4])
  
def p_while(p):
  '''while : WHILE'''
  global loopingDepth
  loopingDepth += 1
  p[0] = p[1]
  p[0] = build_AST(p)

def p_iteration_statement_2(p):
    '''iteration_statement : do statement WHILE LPAREN expression RPAREN SEMICOLON'''
    p[0] = Node(name = 'DoWhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
    global loopingDepth
    loopingDepth -= 1
    p[0].ast = build_AST(p,[4,6])

def p_do(p):
  '''do : DO'''
  global loopingDepth
  loopingDepth += 1
  p[0] = p[1]
  p[0] = build_AST(p)

def p_iteration_statement_3(p):
    '''iteration_statement : for LPAREN expression_statement expression_statement RPAREN statement'''
    p[0] = Node(name = 'ForWithoutStatement', val = '', type = '', children = [], lno = p.lineno(1))
    global loopingDepth
    loopingDepth -= 1
    p[0].ast = build_AST(p,[2,5])

def p_iteration_statement_4(p):
    '''iteration_statement : for LPAREN expression_statement expression_statement expression RPAREN statement'''
    p[0] = Node(name = 'ForWithStatement', val = '', type = '', children = [], lno = p.lineno(1)) 
    global loopingDepth
    loopingDepth -= 1
    p[0].ast = build_AST(p,[2,6])

def p_for(p):
  '''for : FOR'''
  global loopingDepth
  loopingDepth += 1
  # p[0] = Node(name = 'ForWithStatement', val = '', type = '', children = [], lno = p.lineno(1))
  p[0] = p[1]
  p[0] = build_AST(p)

def p_jump_statement(p):
    '''jump_statement : RETURN SEMICOLON
                      | RETURN expression SEMICOLON
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 3):
      p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])
      p[0].ast = build_AST(p,[2])
      if(curFuncReturnType != 'void'):
        print('COMPILATION ERROR at line ' + str(p.lineno(1)) + ': function return type is not void')
    else:
      # print(p[2].type,curFuncReturnType)
      if(p[2].type != '' and curFuncReturnType != p[2].type):
        # print(curFuncReturnType)
        print('warning at line ' + str(p.lineno(1)) + ': function return type is not ' + p[2].type)
      p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])   
      p[0].ast = build_AST(p,[2]) 

def p_jump_statement_1(p):
  '''jump_statement : BREAK SEMICOLON'''
  global loopingDepth
  global switchDepth
  p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])
  p[0].ast = build_AST(p,[2])
  if(loopingDepth == 0 and switchDepth == 0):
    print(p[0].lno, 'break not inside loop')

def p_jump_statement_2(p):
  '''jump_statement : CONTINUE SEMICOLON'''
  global loopingDepth

  p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])
  p[0].ast = build_AST(p,[2])

  if(loopingDepth == 0):
    print(p[0].lno, 'continue not inside loop')

def p_jump_statement_3(p):
  '''jump_statement : GOTO ID SEMICOLON'''
  p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = []) 
  p[0].ast = build_AST(p,[3])   

def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])
    if(len(p) == 2):
      p[0].children.append(p[1])
    else:
      p[0].children.append(p[2])
    p[0].ast = build_AST(p)
    
    

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration
    '''
    p[0] = p[1]
    p[0].name = 'ExternalDeclaration'
    p[0].ast = build_AST(p)
    #p[0] = Node()

def p_function_definition_1(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement
                           | declarator declaration_list function_compound_statement
                           | declarator function_compound_statement                                                                              
    ''' 
    #p[0] = Node()
    # p[0] = build_AST(p)  
    if(len(p) == 3):
      p[0] = Node(name = 'FuncDeclWithoutType',val = p[1].val,type = 'int', lno = p[1].lno, children = [])
    elif(len(p) == 4):
      p[0] = Node(name = 'FuncDeclWithoutType',val = p[1].val,type = 'int', lno = p[1].lno, children = [])
    else:
      # no need to keep type in AST
      p[0] = Node(name = 'FuncDecl',val = p[2].val,type = p[1].type, lno = p[1].lno, children = [])
    p[0].ast = build_AST(p)


def p_function_definition_2(p):
  '''function_definition : declaration_specifiers declarator function_compound_statement'''


  p[0] = Node(name = 'FuncDecl',val = p[2].val,type = p[1].type, lno = p.lineno(1), children = [])
  p[0].ast = build_AST(p)

def p_openbrace(p):
  '''openbrace : LCURLYBRACKET'''
  global currentScope
  global nextScope
  parent[nextScope] = currentScope
  currentScope = nextScope
  symbol_table.append({})
  nextScope = nextScope + 1
  p[0] = p[1]

def p_lopenparen(p):
  '''lopenparen : LPAREN'''
  global currentScope
  global nextScope
  parent[nextScope] = currentScope
  currentScope = nextScope
  symbol_table.append({})
  nextScope = nextScope + 1
  p[0] = p[1]

def p_closebrace(p):
  '''closebrace : RCURLYBRACKET'''
  global currentScope
  currentScope = parent[currentScope]
  p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    # print(p)
    if(p):
      print("Syntax error in input at line " + str(p.lineno))
    # p.lineno(1)

def runmain(code):
  open('graph1.dot','w').write("digraph G {")
  parser = yacc.yacc(start = 'translation_unit')
  result = parser.parse(code,debug=True)
  open('graph1.dot','a').write("\n}")
  visualize_symbol_table()

  graphs = pydot.graph_from_dot_file('graph1.dot')
  # print(len(graphs))
  graph = graphs[0]
  graph.write_png('pydot_graph.png')

def visualize_symbol_table():
  global scopeName
  for i in range (nextScope):
    if(len(symbol_table[i]) > 0):
      print('\nIn Scope ' + str(i))
      for key in symbol_table[i].keys():
        print(key, symbol_table[i][key])
      # json_object = json.dumps(symbol_table[i], indent = 4)
      # print(json_object)
