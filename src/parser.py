# Yacc example

import ply.yacc as yacc
import sys
import pydot

# Get the token map from the lexer.  This is required.
from lexer import tokens
precedence = (
     ('nonassoc', 'IFX'),
     ('nonassoc', 'ELSE')
 )

symbol_table = []
symbol_table.append({'parent_scope_name':'','scope_name':'s0'})
symbol_table[0]['printInt'] = ['int', 'Function 1', -1, {}, 4,[],-1,[]]
symbol_table[0]['printString'] = ['int', 'Function 1', -1, {}, 4,[],-1,[]]
currentScope = 0
nextScope = 1
parent = []

class Node:
  def __init__(self,name = '',val = '',lno = 0,type = '',children = '',scope = 0):
    self.name = name
    self.val = val
    self.type = type
    self.lineno = lno
    self.scope = scope
    if children:
      self.children = children
    else:
      self.children = []
    
    # add more later

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
def p_primary_expression_1(p):
  '''primary_expression : ID 
                | OCTAL_CONST
                | HEX_CONST
                | BIN_CONST
                | LPAREN expression RPAREN
  '''
  # p[0] = build_AST(p)
  if(len(p) == 3):
    p[0] = p[2]
    # p[0].name = 'primaryExpression'
  else:
    p[0] = Node(name = 'primaryExpression',val = p[1],lno = p.lineno(1),type = '',children = [])
    

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

def p_postfix_expression_3(p):
  '''postfix_expression : postfix_expression LPAREN RPAREN'''
  p[0] = Node(name = 'FunctionCall',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1]])
  
def p_postfix_expression_4(p):
  '''postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'''
  p[0] = Node(name = 'FunctionCall2',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1],p[3]])

def p_postfix_expression_5(p):
  '''postfix_expression : postfix_expression PERIOD ID
  | postfix_expression ARROW ID'''
  # no period in ast, but ID should always be present, making a tempNode to show 
  # ID as child of p[0].
  tempNode = Node(name = '',val = p[3],lno = p[1].lno,type = '',children = '')
  p[0] = Node(name = 'PeriodOrArrowExpression',val = tempNode.val,lno = tempNode.lno,type = tempNode.type,children = [p[1],tempNode])

def p_postfix_expression_6(p):
  '''postfix_expression : postfix_expression INCREMENT
	| postfix_expression DECREMENT'''
  tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
  p[0] = Node(name = 'IncrementOrDecrementExpression',val = p[1].val,lno = p[1].lno,type = p[1].type,children = [p[1],tempNode])


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


def p_unary_expression_2(p):
  '''unary_expression : unary_operator cast_expression'''
  # p[1] can be &,*,+,-,~,!
  # p[0] = Node(name = 'UnaryOperation',val = p[2].val,lno = p[2].lno,type = p[2].type,children = [tempNode,p[2]])
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
    if(p[2] == '%'):
      p[0] = Node(name = 'Mod',val = p[1].val,lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])
    else:
      p[0] = Node(name = 'MulDiv',val = p[1].val,lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

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
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'AddSub',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

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
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'Shift',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

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
    tempNode = Node(name = '',val = p[2],lno = p[1].lno,type = '',children = '')
    p[0] = Node(name = 'RelationalOperation',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

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
    p[0] = Node(name = 'EqualityOperation',val = '',lno = p[1].lno,type = '',children = [p[1],tempNode,p[3]])

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
    tempNode = Node(name = '',val = p[2],type = '', lno = p[1].lineno, children = [])
    p[0] = Node(name = 'AssignmentOperation',val = '',type = p[1].type, lno = p[1].lineno, children = [p[1],tempNode,p[3]])
    find_if_ID_is_declared(p[1].val, p[1].lineno)

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
  p[0] = p[1]
  # p[0] = Node(name = '',val = '',type = p[1].type, lno = p[1].lno, children = [p[1],p[2],p[3]])

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
    a = 1
    #fill later

def p_declaration_specifiers(p):
  '''declaration_specifiers : storage_class_specifier
	| storage_class_specifier declaration_specifiers
	| type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
  '''
  a = 1
  #p[0] = Node()
  # p[0] = build_AST(p)




def p_init_declarator_list(p):
  '''init_declarator_list : init_declarator
	| init_declarator_list COMMA init_declarator
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  if(len(p) == 2):
    p[0] = p[1]
  else:
    #check once
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
  else:
    tempNode = Node(name = '',val = p[2],type = '', lno = p[1].lno, children = [])
    p[0] = Node(name = 'DeclWithIntialization',val = '',type = p[1].type, lno = p[1].lno, children = [p[1],tempNode,p[3]])

def p_storage_class_specifier(p):
  '''storage_class_specifier : TYPEDEF
	| EXTERN
	| STATIC
	| AUTO
	| REGISTER
  '''
  #p[0] = Node()
  # p[0] = build_AST(p)
  p[0] = p[1]
  # p[0] = Node(name = 'DeclWithIntialization',val = '',type = p[1].type, lno = p[1].lno, children = [p[1],tempNode,p[3]])


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
  p[0] = Node(name = '',val = '',type = p[1], lno = p.lineno(1), children = [])

def p_type_specifier_2(p):
  '''type_specifier : struct_or_union_specifier
                    | enum_specifier '''
  p[0] = p[1]

def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier : struct_or_union ID openbrace struct_declaration_list closebrace
  | struct_or_union openbrace struct_declaration_list closebrace
  | struct_or_union ID
  '''
  # p[0] = build_AST(p)

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
  p[0] = build_AST(p)

def p_struct_declaration(p):
  '''struct_declaration : specifier_qualifier_list struct_declarator_list SEMICOLON
  '''
  p[0] = build_AST(p)

def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list : type_specifier specifier_qualifier_list
  | type_specifier
  | type_qualifier specifier_qualifier_list
  | type_qualifier
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_struct_declarator_list(p):
  '''struct_declarator_list : struct_declarator
	| struct_declarator_list COMMA struct_declarator
  '''
  p[0] = build_AST(p)

def p_struct_declarator(p):  
  '''struct_declarator : declarator
	| COLON constant_expression
	| declarator COLON constant_expression
  '''
  p[0] = build_AST(p)

def p_enum_specifier(p):
  '''enum_specifier : ENUM openbrace enumerator_list closebrace
	| ENUM ID openbrace enumerator_list closebrace
	| ENUM ID
  '''
  p[0] = build_AST(p)

def p_enumerator_list(p):
  '''enumerator_list : enumerator
	| enumerator_list COMMA enumerator
  '''
  p[0] = build_AST(p)

def p_enumerator(p):
  '''enumerator : ID
	| ID EQUALS constant_expression
	'''
  p[0] = build_AST(p)

def p_type_qualifier(p):
    '''type_qualifier : CONST
                      | VOLATILE
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_declarator(p):
  '''declarator : pointer direct_declarator
  | direct_declarator
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_direct_declarator(p):
  '''direct_declarator : ID
                        | LPAREN declarator RPAREN
                        | direct_declarator LSQUAREBRACKET constant_expression RSQUAREBRACKET
                        | direct_declarator LSQUAREBRACKET RSQUAREBRACKET
                        | direct_declarator LPAREN parameter_type_list RPAREN
                        | direct_declarator LPAREN identifier_list RPAREN
                        | direct_declarator LPAREN RPAREN
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_pointer(p):
  '''pointer : MULTIPLY 
              | MULTIPLY type_qualifier_list
              | MULTIPLY pointer
              | MULTIPLY type_qualifier_list pointer
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_type_qualifier_list(p):
  '''type_qualifier_list : type_qualifier
                        | type_qualifier_list type_qualifier
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_parameter_type_list(p):
  '''parameter_type_list : parameter_list
                          | parameter_list COMMA ELLIPSIS
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_parameter_list(p):
    '''parameter_list : parameter_declaration
                      | parameter_list COMMA parameter_declaration
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator
                             | declaration_specifiers abstract_declarator
                             | declaration_specifiers
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

# symbolTable['varName'][3] = {}


def p_identifier_list(p):
    '''identifier_list : ID
                       | identifier_list COMMA ID
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_type_name(p):
    '''type_name : specifier_qualifier_list
                 | specifier_qualifier_list abstract_declarator
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_abstract_declarator(p):
    '''abstract_declarator : pointer 
                           | direct_abstract_declarator
                           | pointer direct_abstract_declarator
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_direct_abstract_declarator(p):
    '''direct_abstract_declarator : LPAREN abstract_declarator RPAREN
                                  | LSQUAREBRACKET RSQUAREBRACKET
                                  | LSQUAREBRACKET constant_expression RSQUAREBRACKET
                                  | direct_abstract_declarator LPAREN RPAREN
                                  | direct_abstract_declarator LPAREN constant_expression RPAREN 
                                  | LPAREN RPAREN
                                  | LPAREN parameter_type_list RPAREN
                                  | direct_abstract_declarator LPAREN parameter_type_list RPAREN
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_initializer(p):
    '''initializer : assignment_expression
                   | openbrace initializer_list closebrace
                   | openbrace initializer_list COMMA closebrace                                   
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_initializer_list(p):
  '''initializer_list : initializer
  | initializer_list COMMA initializer
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_statement(p):
    '''statement : labeled_statement
                 | compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
    '''symbol_table.append({'parent_scope_name':'','scope_name':'s0'})
def p_labeled_statement(p):
    '''labeled_statement : ID COLON statement 
                         | CASE constant_expression COLON statement
                         | DEFAULT COLON statement
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_compound_statement(p):
    '''compound_statement : openbrace closebrace
                          | openbrace statement_list closebrace
                          | openbrace declaration_list closebrace
                          | openbrace declaration_list statement_list closebrace
    '''  
    #p[0] = Node()
    p[0] = build_AST(p)                        

def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_expression_statement(p):
    '''expression_statement : SEMICOLON
                            | expression SEMICOLON
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_selection_statement(p):
    '''selection_statement : IF LPAREN expression RPAREN statement %prec IFX
                           | IF LPAREN expression RPAREN statement ELSE statement
                           | SWITCH LPAREN expression RPAREN statement
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_iteration_statement(p):
    '''iteration_statement : WHILE LPAREN expression RPAREN
                           | DO statement WHILE LPAREN expression RPAREN SEMICOLON
                           | FOR LPAREN expression_statement expression_statement RPAREN statement
                           | FOR LPAREN expression_statement expression_statement expression RPAREN statement                                                 
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_jump_statement(p):
    '''jump_statement : GOTO ID SEMICOLON
                      | CONTINUE SEMICOLON
                      | BREAK SEMICOLON
                      | RETURN SEMICOLON
                      | RETURN expression SEMICOLON
    '''
    #p[0] = Node()
    # p[0] = build_AST(p)
    tempNode = Node(name = '',val = p[1],type = '', lno = p.lineno(1), children = [])
    tempNode2 = Node(name = '',val = p[2],type = '', lno = p.lineno(1), children = [])
    if(len(p) == 3):
      p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [tempNode,tempNode2])
    else:
      tempNode3 = Node(name = '',val = p[3],type = '', lno = p.lineno(1), children = [])
      p[0] = Node(name = 'JumpStatement',val = '',type = '', lno = p.lineno(1), children = [tempNode,tempNode2,tempNode3])    

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
    #p[0] = Node()
    # p[0] = build_AST(p)

def p_function_definition_1(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement
                           | declarator declaration_list compound_statement
                           | declarator compound_statement                                                                              
    ''' 
    #p[0] = Node()
    # p[0] = build_AST(p)  
    if(len(p) == 3):
      p[0] = Node(name = 'FuncDeclWithoutType',val = p[1].val,type = p[1].type, lno = p[1].lno, children = [p[1],p[2]])
    elif(len(p) == 4):
      p[0] = Node(name = 'FuncDeclWithoutType',val = p[1].val,type = p[1].type, lno = p[1].lno, children = [p[1],p[2],p[3]])
    else:
      # no need to keep type in AST
      p[0] = Node(name = 'FuncDecl',val = p[2].val,type = p[1].type, lno = p[1].lno, children = [p[2],p[3],p[4]])

def p_function_definition_2(p):
  '''function_definition : declaration_specifiers declarator compound_statement'''
  # no need to keep type in AST
  p[0] = Node(name = 'FuncDecl',val = p[2].val,type = p[1].type, lno = p[1].lno, children = [p[2],p[3]])

def p_openbrace(p):
  '''openbrace : LCURLYBRACKET'''
  global currentScope
  global nextScope
  parent[nextScope] = currentScope
  currentScope = nextScope
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
  result = parser.parse(code)
  open('graph1.dot','a').write("\n}")

  graphs = pydot.graph_from_dot_file('graph1.dot')
  # print(len(graphs))
  graph = graphs[0]
  graph.write_png('pydot_graph.png')

  # print(result)
  # while True:
  #   # try:
  #   #   s = input('calc > ')
  #   # except EOFError:
  #   #   break
  #   # z = code.readlines()
  #   if not s: continue
  #   print(s)
  #   result = parser.parse(s,debug=True)
  #   print(result)
