# Yacc example

import ply.yacc as yacc
import sys
import pydot
import copy

# Get the token map from the lexer.  This is required.
from lexer import tokens
precedence = (
     ('nonassoc', 'IFX'),
     ('nonassoc', 'ELSE')
 )

symbol_table = []
symbol_table.append({})
currentScope = 0
nextScope = 1
parent = {}
parent[0] = 0
class Node:
  def __init__(self,name = '',val = '',lno = 0,type = '',children = '',scope = 0, array = [] ):
    self.name = name
    self.val = val
    self.type = type
    self.lno = lno
    self.scope = scope
    self.array = array
    if children:
      self.children = children
    else:
      self.children = []
    
    # add more later
ts_unit = Node('START',val = '',type ='' ,children = [])

def get_higher_data_type(type_1 , type_2):
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

  num_type_1 = to_num[type_1]
  num_type_2 = to_num[type_2]
  return to_str[max(num_type_1 , num_type_2)]



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
  return False

def find_if_ID_is_declared(id,lineno):
  curscp = currentScope
  # print("here" + str(curscp))
  while(parent[curscp] != curscp):
    # print("here" + str(curscp))
    if(id in symbol_table[curscp].keys()):
      return 1
    curscp = parent[curscp]
  if (curscp == 0):
    if(id in symbol_table[curscp].keys()):
      return 1
  print (lineno, 'COMPILATION ERROR: unary_expression ' + id + ' not declared')
  return 0



cur_num = 0

def build_AST(p):
  global cur_num
  calling_func_name = sys._getframe(1).f_code.co_name
  calling_rule_name = calling_func_name[2:]
  length = len(p)
  if(length == 2):
    return p[1]
  else:
    cur_num += 1
    p_count = cur_num
    open('graph1.dot','a').write("\n" + str(p_count) + "[label=\"" + calling_rule_name.replace('"',"") + "\"]") ## make new vertex in dot file
    for child in range(1,length,1):
      global child_num 
      global child_val
      if(type(p[child]) is tuple):
        if(ignore_1(p[child][0]) is False):
          open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child][1]))
      else:
        if(ignore_1(p[child]) is False):
          cur_num += 1
          open('graph1.dot','a').write("\n" + str(cur_num) + "[label=\"" + str(p[child]).replace('"',"") + "\"]")
          p[child] = (p[child],cur_num)
          open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child][1]))
    return (calling_rule_name,p_count)

# name = '',val = '',lno = 0,type = '',children = '',pydot_info = None

#ToDo : think how to deal with octal, hex and bin const
#if reduces to ID, check if it is present in symbol table
def p_primary_expression_0(p):
  '''primary_expression : ID'''
  p[0] = Node(name = 'PrimaryExpression',val = p[1],lno = p.lineno(1),type = '',children = [])
  find_if_ID_is_declared(p[1],p.lineno(1))

def p_primary_expression_1(p):
  '''primary_expression : OCTAL_CONST
                | HEX_CONST
                | BIN_CONST
                | LPAREN expression RPAREN
  '''
  # p[0] = build_AST(p)
  if(len(p) == 4):
    p[0] = p[2]
    # p[0].name = 'primaryExpression'
  else:
    p[0] = Node(name = 'PrimaryExpression',val = p[1],lno = p.lineno(1),type = '',children = [])
    

def p_primary_expression_2(p):
  '''primary_expression : CHAR_CONST'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'char',children = [])

def p_primary_expression_3(p):
  '''primary_expression : INT_CONST'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'int',children = [])

def p_primary_expression_4(p):
  '''primary_expression : FLOAT_CONST'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'float',children = [])

def p_primary_expression_5(p):
  '''primary_expression : STRING_LITERAL'''
  p[0] = Node(name = 'ConstantExpression',val = p[1],lno = p.lineno(1),type = 'string',children = [])

########################

def p_postfix_expression_1(p):
  '''postfix_expression : primary_expression'''
  #p[0] = Node()
  # p[0] = build_AST(p)
  p[0] = p[1]

def p_postfix_expression_2(p):
  '''postfix_expression : postfix_expression LSQUAREBRACKET expression RSQUAREBRACKET'''
  # check if value should be p[1].val
  p[0] = Node(name = 'ArrayExpression',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1],p[3]])
  curscp = currentScope
  if(p[3].type not in ['char', 'short', 'int', 'long']):
    print("Compilation Error: Array index at line ", p[3].lno, " is not of compatible type")

def p_postfix_expression_3(p):
  '''postfix_expression : postfix_expression LPAREN RPAREN'''
  p[0] = Node(name = 'FunctionCall1',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1]])
  # find_if_ID_is_declared(p[1].val,p[1].lno)


def p_postfix_expression_4(p):
  '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
  p[0] = Node(name = 'FunctionCall2',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1],p[3]])
  # find_if_ID_is_declared(p[1].val,p[1].lno)
  #check if function argument_list_expression matches with the actual one
  


def p_postfix_expression_5(p):
  '''postfix_expression : postfix_expression PERIOD ID
  | postfix_expression ARROW ID'''
  # no period in ast, but ID should always be present, making a tempNode to show 
  # ID as child of p[0].
  tempNode = Node(name = '',val = p[3],lno = p[1].lno,type = '',children = '')
  p[0] = Node(name = 'PeriodOrArrowExpression',val = tempNode.val,lno = tempNode.lno,type = tempNode.type,children = [p[1],tempNode])
  # structure things , do later



def p_postfix_expression_6(p):
  '''postfix_expression : postfix_expression INCREMENT
	| postfix_expression DECREMENT'''
  tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
  p[0] = Node(name = 'IncrementOrDecrementExpression',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1],tempNode])
  #Can't think of a case where this is invalid



#################

def p_argument_expression_list(p):
  '''argument_expression_list : assignment_expression
                              | argument_expression_list COMMA assignment_expression
  '''
  if(len(p) == 2):
    #left val empty here for now
    p[0] = Node(name = 'ArgumentExpressionList',val = '',lno = p[1].lno,type = p[1].type,children = [p[1]])
  else:
    #check if name will always be equal to ArgumentExpressionList
    # heavy doubt
    p[0] = p[1]
    p[0].children.append(p[3])
    # for child in p[0].children:
    #   print(child.type)
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
  else:
    #check lineno
    #also check if child should be added or not
    tempNode = Node(name = '',val = p[1],lno = p[2].lno,type = '',children = '')
    p[0] = Node(name = 'UnaryOperation',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [tempNode,p[2]])
    #Can't think of a case where this is invalid

def p_unary_expression_2(p):
  '''unary_expression : unary_operator cast_expression'''
  # p[1] can be &,*,+,-,~,!
  if(p[1] == '&'):
    # no '&' child added, will deal in traversal
    p[0] = Node(name = 'AddressOfVariable',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])
  elif(p[1] == '*'):
    p[0] = Node(name = 'PointerVariable',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])
  elif(p[1] == '-'):
    p[0] = Node(name = 'UnaryOperationMinus',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])
  else:
    tempNode = Node(name = '',val = p[1],lno = p[2].lno,type = '',children = '')
    p[0] = Node(name = 'UnaryOperation',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [tempNode,p[2]])

def p_unary_expression_3(p):
  '''unary_expression : SIZEOF unary_expression'''
  # should I add SIZEOF in children
  p[0] = Node(name = 'SizeOf',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2]])

def p_unary_expression_4(p):
  '''unary_expression : SIZEOF LPAREN type_name RPAREN'''
  # should I add SIZEOF in children
  p[0] = Node(name = 'SizeOf',val = p[3].val,lno = p[3].lno,type = p[3].type,children = [p[3]])

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
  p[0] = p[1]

#################

def p_cast_expression(p):
  '''cast_expression : unary_expression
                     | LPAREN type_name RPAREN cast_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    # confusion about val
    p[0] = Node(name = 'TypeCasting',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [p[2],p[4]])

################

#No type should be passed in below cases since multiplication, division, add, sub work
# for all types that are present in C.

# def p_multipicative_expression(p):
#   '''multiplicative_expression : cast_expression
# 	| multiplicative_expression MULTIPLY cast_expression
# 	| multiplicative_expression DIVIDE cast_expression
# 	| multiplicative_expression MOD cast_expression
#   '''
#   #p[0] = Node()
#   # p[0] = build_AST(p)
#   if(len(p) == 2):
#     p[0] = p[1]
#   else:
#     # val empty 
#     tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
#     if(p[2] == '%'):
#       p[0] = Node(name = 'Mod',val = p[1].val,lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])
#     else:
#       p[0] = Node(name = 'MulDiv',val = p[1].val,lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])



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
  else:
    # val empty 
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')

    type_list = ['char' , 'short' , 'int' , 'long' , 'float' , 'double']
    if(p[1].type not in type_list or p[3].type not in type_list):
      print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
    
    if(p[2] == '%'):
      valid_type = ['char' , 'short' , 'int' , 'long']
      higher_data_type = get_higher_data_type(p[1].type , p[3].type)
      
      if higher_data_type not in valid_type:
        print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with MOD operator')

      return_data_type = higher_data_type
      if return_data_type == 'char' :
        return_data_type = 'int'
      p[0] = Node(name = 'Mod',val = p[1].val,lno = p[1].lno,type = return_data_type,children = [p[1],tempNode,p[3]])

    else:
      higher_data_type = get_higher_data_type(p[1].type , p[3].type)
      return_data_type = higher_data_type
      if return_data_type == 'char' :
        return_data_type = 'int'
      p[0] = Node(name = 'MulDiv',val = p[1].val,lno = p[1].lno,type = return_data_type,children = [p[1],tempNode,p[3]])

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
  else:
    type_list = ['char' , 'short' , 'int' , 'long' , 'float' , 'double']
    if p[1].type not in type_list or p[3].type not in type_list:
      print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')
    
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    higher_data_type = get_higher_data_type(p[1].type , p[3].type)
    p[0] = Node(name = 'AddSub',val = '',lno = p[1].lno,type = higher_data_type,children = [p[1],tempNode,p[3]])

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
  else:
    # We know shift only possible in int(unsigned) type, so no need to pass for now
    type_list = ['short' , 'int' , 'long']
    if p[1].type not in type_list or p[3].type not in type_list:
      print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')

    higher_data_type = get_higher_data_type(p[1].type , p[3].type)
    p[0] = Node(name = 'Shift',val = '',lno = p[1].lno,type = higher_data_type,children = [p[1],tempNode,p[3]])

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
  else:
    type_list = ['char' , 'short' , 'int' , 'long' , 'float' , 'double']
    if p[1].type not in type_list or p[3].type not in type_list:
      print(p[1].lno , 'COMPILATION ERROR : Incompatible data type with ' + p[2] +  ' operator')

    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'RelationalOperation',val = '',lno = p[1].lno,type = 'int',children = [p[1],tempNode,p[3]])

def p_equality_expresssion(p):
  '''equality_expression : relational_expression
	| equality_expression EQUAL relational_expression
	| equality_expression NOTEQUAL relational_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'EqualityOperation',val = '',lno = p[1].lno,type = 'int',children = [p[1],tempNode,p[3]])

def p_and_expression(p):
  '''and_expression : equality_expression
	| and_expression AND equality_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'AndOperation',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])
    valid = ['int', 'char'] #TODO: check this if more AND should be taken
    if p[1].type not in valid or p[3].type not in valid:
      print(p[1].lno , 'COMPILATION ERROR : Incompatible data types', p[1].type, 'and', p[2].type, 'for the AND operator')
    else:
      p[0].type = 'int' # should not be char, even if the and was done for two chars

def p_exclusive_or_expression(p):
  '''exclusive_or_expression : and_expression
	| exclusive_or_expression XOR and_expression
	'''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'XorOperation',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

def p_inclusive_or_expression(p):
  '''inclusive_or_expression : exclusive_or_expression
	| inclusive_or_expression OR exclusive_or_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'OrOperation',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

def p_logical_and_expression(p):
  '''logical_and_expression : inclusive_or_expression 
  | logical_and_expression LAND inclusive_or_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'LogicalAndOperation',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

def p_logical_or_expression(p):
  '''logical_or_expression : logical_and_expression
	| logical_or_expression LOR logical_and_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'LogicalOrOperation',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

def p_conditional_expression(p):
  '''conditional_expression : logical_or_expression
	| logical_or_expression CONDOP expression COLON conditional_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    # tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    #check type and shoul COLON, CONDOP be passed as children
    p[0] = Node(name = 'ConditionalOperation',val = '',lno = p[1].lno,type = '',children = [p[1],p[3],p[5]])


def p_assignment_expression(p):
  '''assignment_expression : conditional_expression 
                           | unary_expression assignment_operator assignment_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    #check children
    # tempNode = Node(name = '',val = p[2],type = '', lno = p[1].lineno, children = [])
    p[0] = Node(name = 'AssignmentOperation',val = '',type = p[1].type, lno = p[1].lno, children = [p[1],p[3]])
    # find_if_ID_is_declared(p[1].val, p[1].lno)

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

def p_expression(p):
  '''expression : assignment_expression
	| expression COMMA assignment_expression
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    # optimized here, might also be possible above somewhere
    p[0] = p[1]
    p[0].children.append(p[3])

def p_constant_expression(p):
  '''constant_expression : conditional_expression'''
  # p[0] = build_AST(p)
  p[0] = p[1]

def p_declaration(p):
  '''declaration : declaration_specifiers SEMICOLON
	| declaration_specifiers init_declarator_list SEMICOLON
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 3):
    p[0] = p[1]
  else:
    # a = 1
    p[0] = Node(name = 'Declaration',val = p[1],type = '', lno = p.lineno(1), children = [])
    #fill later
    for child in p[2].children:
      if(child.name == 'InitDeclarator'):
        if(child.children[0].val in symbol_table[currentScope].keys()):
          print(p.lineno(1), 'COMPILATION ERROR : ' + child.children[0].val + ' already declared')
        # print(child.children[0].val,child.children[1].val)
        symbol_table[currentScope][child.children[0].val] = {}
        symbol_table[currentScope][child.children[0].val]['type'] = p[1].type
        symbol_table[currentScope][child.children[0].val]['value'] = child.children[1].val
        if(len(child.children[0].array) > 0):
          symbol_table[currentScope][child.children[0].val]['array'] = child.children[0].array
        if(len(child.children[0].type) > 0):
          symbol_table[currentScope][child.children[0].val]['type'] = p[1].type + ' ' + child.children[0].type 
      else:
        if(child.val in symbol_table[currentScope].keys()):
          print(p.lineno(1), 'COMPILATION ERROR : ' + child.val + ' already declared')
        symbol_table[currentScope][child.val] = {}
        symbol_table[currentScope][child.val]['type'] = p[1].type
        if(len(child.array) > 0):
          symbol_table[currentScope][child.val]['array'] = child.array
        if(len(child.type) > 0):
          symbol_table[currentScope][child.val]['type'] = p[1].type + ' ' + child.type

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
  elif(len(p) == 3):
    if(p[1].name == 'StorageClassSpecifier' and p[2].name.startswith('StorageClassSpecifier')):
      print("Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type)
    if(p[1].name == 'TypeSpecifier1' and (p[2].name.startswith('TypeSpecifier1') or p[2].name.startswith('StorageClassSpecifier') or p[2].name.startswith('TypeQualifier'))):
      print("Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type)
    if(p[1].name == 'TypeQualifier' and (p[2].name.startswith('StorageClassSpecifier') or p[2].name.startswith('TypeQualifier'))):
      print("Invalid Syntax at line " + str(p[1].lno) + ", " + p[2].type + " not allowed after " + p[1].type)
    # if(p[1].name == '')
    p[0] = Node(name = p[1].name + p[2].name,val = p[1],type = p[1].type + ' ' + p[2].type, lno = p[1].lno, children = [])
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
  else:
    #check onceƒ
    p[0] = p[1]
    p[0].children.append(p[3])

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
    p[0].name = 'InitDeclarator'
  else:
    # tempNode = Node(name = '',val = p[2],type = '', lno = p[1].lno, children = [])
    p[0] = Node(name = 'InitDeclarator',val = '',type = p[1].type,lno = p.lineno(1), children = [p[1],p[3]], array = p[1].array)

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

def p_type_specifier_2(p):
  '''type_specifier : struct_or_union_specifier
                    | enum_specifier '''
  p[0] = p[1]
  # p[0] = Node(name = '',val = '',type = p[1], lno = p.lineno(1), children = [])

def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier : struct_or_union ID openbrace struct_declaration_list closebrace
  | struct_or_union openbrace struct_declaration_list closebrace
  | struct_or_union ID
  '''
  # p[0] = build_AST(p)
  # TODO : check the semicolon thing after closebrace in gramamar
  p[0] = Node(name = 'StructOrUnionSpecifier', val = '', type = p[1].type, lno = p[1].lno , children = [])

def p_struct_or_union(p):
  '''struct_or_union : STRUCT
	| UNION
  '''
  # p[0] = build_AST(p)
  p[0] = p[1]

def p_struct_declaration_list(p):
  '''struct_declaration_list : struct_declaration
	| struct_declaration_list struct_declaration
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'StructDeclarationList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  if(len(p) == 2):
    p[0].children.append(p[1])
  else:
    p[0].children.append(p[2])


def p_struct_declaration(p):
  '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'StructDeclaration', val = '', type = 'struct_declaration', lno = p[1].lno, children = [])

def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list : type_specifier specifier_qualifier_list
  | type_specifier
  | type_qualifier specifier_qualifier_list
  | type_qualifier
  '''
  #p[0] = Node()
  #p[0] = build_AST(p)
  p[0] = Node(name = 'SpecifierQualifierList', val = '', type = p[1].type, lno = p[1].lno, children = [])


def p_struct_declarator_list(p):
  '''struct_declarator_list : struct_declarator
	| struct_declarator_list COMMA struct_declarator
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'StructDeclaratorList', val = '', type = p[1].type, lno = p[1].lno, children = [])
  if(len(p) == 2):
    p[0].children.append(p[1])
  else:
    p[0].children.append(p[3])

def p_struct_declarator(p):  
  '''struct_declarator : declarator
	| COLON constant_expression
	| declarator COLON constant_expression
  '''
  #p[0] = build_AST(p)
  if len(p) == 2 or len(p) == 4:
    p[0] = p[1] 
  if len(p) == 3:
    p[0] = p[2]
  

def p_enum_specifier(p):
  '''enum_specifier : ENUM openbrace enumerator_list closebrace
	| ENUM ID openbrace enumerator_list closebrace
	| ENUM ID
  '''
  #p[0] = build_AST(p)
  if(len(p) == 5):
    p[0] = Node(name = 'EnumSpecifier', val = '', type = 'Enum_Specifier', lno = p[3].lno, children = [])
  elif(len(p) == 6):
    p[0] = Node(name = 'EnumSpecifier', val = '', type = 'Enum_Specifier', lno = p[4].lno, children = [])
  else:
    p[0] = Node(name = 'EnumSpecifier', val = '', type = 'Enum_Specifier', lno = p[2].lno, children = [])

def p_enumerator_list(p):
  '''enumerator_list : enumerator
	| enumerator_list COMMA enumerator
  '''
  #p[0] = build_AST(p)
  p[0] = Node(name = 'EnumeratorList', val= '', type = p[1].type, lno = p[1].lno, children = [])
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
  # print(p[1].children)
  # p[0] = Node(name = 'Declarator', val = '', type = '', lno = p.lineno(1), children = [])
  if(len(p) == 2):
    p[0] = p[1]
    p[0].name = 'Declarator'
    p[0].val = p[1].val
    p[0].array = p[1].array
  else:
    p[0] = p[2]
    p[0].name = 'Declarator'
    p[0].type = p[1].type
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
  if(len(p) == 2):
    p[0] = Node(name = 'ID', val = p[1], type = '', lno = p.lineno(1), children = [])
    # p[0].val = p[1]
    # # insert in symbol table here
    # if(p[1] in symbol_table[currentScope].keys()):
    #   print( 'COMPILATION ERROR at line : ' + p.lineno(1) + ", " + p[1] + ' already declared')

  elif(len(p) == 3):
    p[0] = p[2]
  else:
    p[0] = p[1]
    p[0].children = p
  if(len (p) == 5 and p[3].name == 'ParameterList'):
    p[0].children = p[3].children
    # print(p[0].children)
    if(p[1].val in symbol_table[parent[currentScope]].keys()):
      print('COMPILATION ERROR : near line ' + str(p[1].lno) + ' function already declared')
    symbol_table[parent[currentScope]][p[1].val] = {}
  #TODO: Handle Children
  #p[0] = build_AST(p)

def p_direct_declarator_2(p):
  '''direct_declarator : direct_declarator LSQUAREBRACKET constant_expression RSQUAREBRACKET'''
  p[0] = Node(name = 'ArrayDeclarator', val = p[1].val, type = '', lno = p.lineno(1),  children = [])
  p[0].array = copy.deepcopy(p[1].array)
  p[0].array.append(p[3].val)

def p_direct_declarator_3(p):
  '''direct_declarator : direct_declarator LSQUAREBRACKET RSQUAREBRACKET
                        | direct_declarator lopenparen RPAREN'''
  p[0] = p[1]
  if(p[3] == ')'):
    if(p[1].val in symbol_table[parent[currentScope]].keys()):
      print('COMPILATION ERROR : near line ' + str(p[1].lno) + ' function already declared')
    symbol_table[parent[currentScope]][p[1].val] = {}

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
  elif(len(p) == 3):
    p[0] = Node(name = 'Pointer',val = '',type = p[2].type + ' *', lno = p.lineno(1), children = [])
  else:
    p[0] = Node(name = 'Pointer',val = '',type = p[2].type + ' *', lno = p[2].lno, children = [])

def p_type_qualifier_list(p):
  '''type_qualifier_list : type_qualifier
                        | type_qualifier_list type_qualifier
  '''
  #p[0] = Node()
  if(len(p) == 2):
    p[0] = p[1]
    p[0].name = 'TypeQualifierList'
    p[0].children = p[1]
  else:
    p[0] = p[1]
    p[0].children.append(p[2])
    p[0].type = p[1].type + " " + p[2].type
    p[0].name = 'TypeQualifierList'
    # p[0] = Node(name = '',val = '',type = '', lno = p[1].lno, children = [])

def p_parameter_type_list(p):
  '''parameter_type_list : parameter_list
                          | parameter_list COMMA ELLIPSIS
  '''
  #p[0] = Node()
  p[0] = p[1]
  # TODO : see what to do in case of ellipsis

def p_parameter_list(p):
    '''parameter_list : parameter_declaration
                      | parameter_list COMMA parameter_declaration
    '''
    #p[0] = Node()
    p[0] = Node(name = 'ParameterList', val = '', type = '', children = [], lno = p.lineno(1))
    if(len(p) == 2):
      p[0].children.append(p[1])
    else:
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
      p[0].name = 'ParameterDeclaration'
    else:
      p[0] = Node(name = 'ParameterDeclaration',val = p[2].val,type = p[1].type, lno = p[1].lno, children = [])
      if(len(p[2].type) > 0):
        p[0].type = p[1].type + ' ' + p[2].type
    if(p[2].name == 'Declarator'):
      if(p[2].val in symbol_table[currentScope].keys()):
        print(p.lineno(1), 'COMPILATION ERROR : ' + p[2].val + ' parameter already declared')
      symbol_table[currentScope][p[2].val] = {}
      symbol_table[currentScope][p[2].val]['type'] = p[1].type
      if(len(p[2].type) > 0):
        symbol_table[currentScope][p[2].val]['type'] = p[1].type + ' ' + p[2].type
      if(len(p[2].array) > 0):
        symbol_table[currentScope][p[2].val]['array'] = p[2].array


def p_identifier_list(p):
    '''identifier_list : ID
                       | identifier_list COMMA ID
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 2):
      p[0] = Node(name = 'IdentifierList',val = p1,type = '', lno = p.lineno(1), children = [p[1]])
    else:
      p[0] = p[1]
      p[0].children.append(p[3])
      p[0].name = 'IdentifierList'

def p_type_name(p):
    '''type_name : specifier_qualifier_list
                 | specifier_qualifier_list abstract_declarator
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 2):
      p[0] = p[1]
      p[0].name = 'TypeName'
    else:
      p[0] = Node(name = 'TypeName',val = '',type = p[1].type, lno = p[1].lno, children = [])

def p_abstract_declarator(p):
    '''abstract_declarator : pointer 
                           | direct_abstract_declarator
                           | pointer direct_abstract_declarator
    '''
    #p[0] = Node()
    if(len(p) == 2):
      p[0] = p[1]
      p[0].name = 'AbstractDeclarator'
    elif(len(p) == 3):
      p[0] = Node(name = 'AbstractDeclarator',val = p[2].val,type = p[1].type + ' *', lno = p[1].lno, children = [])

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
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'DirectAbstractDeclarator1'
    else:
      p[0] = Node(name = 'DirectAbstractDeclarator1',val = p[1].val,type = p[1].val, lno = p[1].lno, children = [p[3]])

def p_direct_abstract_declarator_2(p):
  '''direct_abstract_declarator : direct_abstract_declarator LPAREN RPAREN'''
  p[0] = Node(name = 'DirectAbstractDEclarator2', val = p[1].val, type = p[1].type, lno = p[1].lno, children = [])

def p_initializer(p):
    '''initializer : assignment_expression
                   | openbrace initializer_list closebrace
                   | openbrace initializer_list COMMA closebrace                                   
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 2):
      p[0] = p[1]
    else:
      p[0] = p[2]
    p[0].name = 'Initializer'

def p_initializer_list(p):
  '''initializer_list : initializer
  | initializer_list COMMA initializer
  '''
  #p[0] = Node()
  if(len(p) == 2):
    p[0] = Node(name = 'InitializerList', val = '', type = '', children = [p[1]], lno = p.lineno(1))
  else:
    p[0] = Node(name = 'InitializerList', val = '', type = '', children = [], lno = p.lineno(1))
    if(p[1].name != 'InitializerList'):
      p[0].children.append(p[1])
    else:
      p[0].children = p[1].children
    p[0].children.append(p[3])

def p_statement(p):
    '''statement : labeled_statement
                 | compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
    '''
    p[0] = p[1]
def p_labeled_statement_1(p):
    '''labeled_statement : ID COLON statement '''
    p[0] = Node(name = 'LabeledStatement', val = '', type ='', children = [], lno = p.lineno(1) )

def p_labeled_statement_2(p):
    '''labeled_statement : CASE constant_expression COLON statement'''
    p[0] = Node(name = 'CaseStatement', val = '', type = '', children = [], lno = p.lineno(1))

def p_labeled_statement_3(p):
    '''labeled_statement : DEFAULT COLON statement'''
    p[0] = Node(name = 'DefaultStatement', val = '', type = '', children = [], lno = p.lineno(1))

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
    elif(len(p) == 4):
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))                        

def p_function_compound_statement(p):
    '''function_compound_statement : LCURLYBRACKET closebrace
                          | LCURLYBRACKET statement_list closebrace
                          | LCURLYBRACKET declaration_list closebrace
                          | LCURLYBRACKET declaration_list statement_list closebrace
    '''  
    #p[0] = Node()
    #TODO : see what to do in in first case
    if(len(p) == 3):
      p[0] = Node(name = 'CompoundStatement',val = '',type = '', lno = p.lineno(1), children = [])
    elif(len(p) == 4):
      p[0] = p[2]
      p[0].name = 'CompoundStatement'
    elif(len(p) == 4):
      p[0] = Node(name = 'CompoundStatement', val = '', type = '', children = [], lno = p.lineno(1))                        


def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration
    '''
    #p[0] = Node()
    if(len(p) == 2):
      p[0] = p[1]
    else:
      p[0] = Node(name = 'DeclarationList', val = '', type = '', children = [], lno = p.lineno(1))
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
      # p[0].name = 'StatementList'
    else:
      p[0] = Node(name = 'StatementList', val='', type='', children = [], lno = p.lineno(1))
      if(p[1].name != 'StatmentList'):
        p[0].children.append(p[1])
      else:
        p[0].children = p[1].children
      p[0].children.append(p[2])

def p_expression_statement(p):
    '''expression_statement : SEMICOLON
                            | expression SEMICOLON
    '''
    p[0] = Node()
    if(len(p) == 3):
      p[0] = p[1]
    p[0].name = 'ExpressionStatement'
    # TODO : see what to do in case of only semicolon in rhs
    # else:
    #   p[0] = Node(name = '',val = '',type = p[1], lno = p.lineno(1), children = [])
    

def p_selection_statement_1(p):
    '''selection_statement : IF LPAREN expression RPAREN statement %prec IFX'''
    #p[0] = Node()
    p[0] = Node(name = 'IfStatment', val = '', type = '', children = [], lno = p.lineno(1))
  
def p_selection_statement_2(p):
    '''selection_statement : IF LPAREN expression RPAREN statement ELSE statement'''
    p[0] = Node(name = 'IfElseStatement', val = '', type = '', children = [], lno = p.lineno(1))

def p_selection_statement_3(p):
    '''selection_statement : SWITCH LPAREN expression RPAREN statement'''
    p[0] = Node(name = 'SwitchStatement', val = '', type = '', children = [], lno = p.lineno(1))

def p_iteration_statement_1(p):
    '''iteration_statement : WHILE LPAREN expression RPAREN'''
    #p[0] = Node()
    p[0] = Node(name = 'WhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
  
def p_iteration_statement_2(p):
    '''iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMICOLON'''
    p[0] = Node(name = 'DoWhileStatement', val = '', type = '', children = [], lno = p.lineno(1))
  
def p_iteration_statement_3(p):
    '''iteration_statement : FOR LPAREN expression_statement expression_statement RPAREN statement'''
    p[0] = Node(name = 'ForWithoutStatement', val = '', type = '', children = [], lno = p.lineno(1))

def p_iteration_statement_4(p):
    '''iteration_statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement'''
    p[0] = Node(name = 'ForWithStatement', val = '', type = '', children = [], lno = p.lineno(1)) 

def p_jump_statement(p):
    '''jump_statement : GOTO ID SEMICOLON
                      | CONTINUE SEMICOLON
                      | BREAK SEMICOLON
                      | RETURN SEMICOLON
                      | RETURN expression SEMICOLON
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 3):
      p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])
    else:
      # tempNode3 = Node(name = '',val = p[3],type = '', lno = p.lineno(1), children = [])
      p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [])    

def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    if(len(p) == 2):
      ts_unit.children.append(p[1])
    else:
      ts_unit.children.append(p[2])
    

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration
    '''
    p[0] = p[1]
    p[0].name = 'ExternalDeclaration'
    #p[0] = Node()

def p_function_definition_1(p):
    '''function_definition : declaration_specifiers declarator declaration_list function_compound_statement
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

def p_function_definition_2(p):
  '''function_definition : declaration_specifiers declarator function_compound_statement'''
  # no need to keep type in AST
  # if(p[2].name != 'ID'):
  #   print("Syntax error near line " + p[2].lno)
  # else:
  # if(p[2].val in symbol_table[currentScope].keys()):
  #   print('COMPILATION ERROR : near line ' + str(p[1].lno) + ' variable already declared')
  symbol_table[currentScope][p[2].val]['type'] = p[1].type
  # print(p[2].children)
  if(len(p[2].type) > 0):
    symbol_table[currentScope][p[2].val]['type'] = p[1].type + ' ' + p[2].type
  if(len(p[2].children) > 0):
    tempList = []
    for child in p[2].children:
      # print(child.type)
      tempList.append(child.type)
    symbol_table[currentScope][p[2].val]['argumentList'] = tempList
    # print("ys")
  # symbol_table[currentScope][p[2].val]['']
  p[0] = Node(name = 'FuncDecl',val = p[2].val,type = p[1].type, lno = p.lineno(1), children = [])


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
      print("Syntax error in input at line" + str(p.lineno))
    # p.lineno(1)

def runmain(code):
  open('graph1.dot','w').write("digraph G {")
  parser = yacc.yacc(start = 'translation_unit')
  result = parser.parse(code,debug=False)
  open('graph1.dot','a').write("\n}")
  visualize_symbol_table()

  graphs = pydot.graph_from_dot_file('graph1.dot')
  # print(len(graphs))
  graph = graphs[0]
  graph.write_png('pydot_graph.png')

def visualize_symbol_table():
  for i in range (nextScope):
    if(len(symbol_table[i]) > 0):
      print('\nIn Scope ' + str(i))
      for key in symbol_table[i].keys():
        print(key, symbol_table[i][key])
