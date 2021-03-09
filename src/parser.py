# Yacc example

import ply.yacc as yacc
import sys
import pydot
# ignore for p[0] thing - ( ) { } ; 

# Get the token map from the lexer.  This is required.
from lexer import tokens

# precedence = (
#         ('left', 'LOR'),
#         ('left', 'LAND'),
#         ('left', 'OR'),
#         ('left', 'XOR'),
#         ('left', 'AND'),
#         ('left', 'EQUAL', 'NOTEQUAL'),
#         ('left', 'GREATER', 'GREATEREQUAL', 'LESS', 'LESSEQUAL'),
#         ('left', 'RSHIFT', 'LSHIFT'),
#         ('left', 'PLUS', 'MINUS'),
#         ('left', 'MULTIPLY', 'DIVIDE', 'MOD')
#     )

# class Node:
#   def __init__(self):
#     self.num = -1
#     self.val = []
#     # add more later

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

# def build_AST(p):
#   global cur_num
#   calling_func_name = sys._getframe(1).f_code.co_name
#   calling_rule_name = calling_func_name[2:]
#   length = len(p)
#   if(length == 2):
#     # print(p[1])
#     return p[1]
#   else:
#     cur_num += 1
#     p_count = cur_num
#     if(p[0] is not Node):
#       #p[0] = Node()
#     p[0].val = calling_rule_name
#     p[0].num = p_count
#     # print(calling_rule_name)
#     open('graph1.dot','a').write("\n" + str(p_count) + "[label=" + calling_rule_name + "]") ## make new vertex in dot file
#     for child in range(1,length,1):
#       global child_num 
#       global child_val
#       if(type(p[child]) is Node):
#         child_num = p[child].num
#         child_val = p[child].val
#       else:
#         # print(p[child])
#         # if(type(p[child]) is Node):
#           # print(p[child].num)
#         child_val = p[child]
#         child_num = -1
#       if(ignore(str(child_val))):
#         continue
#       if(len(p) == 2):
#         return p[1];
#       else:
#         if(child_num != -1):
#           open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child].num)) ## insert edge between child and par vertex
#         else:
#           # now this node has not been made in dot file
#           cur_num += 1
#           child_num = cur_num
#           # print(child_val)
#           open('graph1.dot','a').write("\n" + str(child_num) + "[label=" + str(child_val) + "]") ## make new vertex in dot file
#           if(type(p[child]) is not Node):
#             p[child] = Node()
#           p[child].num = child_num
#           p[child].val = child_val
#           open('graph1.dot','a').write("\n" + str(p_count) + " -> " + str(p[child].num)) ## insert edge between child and par vertex
#         return p[0]

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


def p_primary_expression(p):
  '''primary_expression : ID
                | CHAR_CONST
                | INT_CONST
                | FLOAT_CONST 
                | OCTAL_CONST
                | HEX_CONST
                | BIN_CONST
                | STRING_LITERAL
                | LPAREN expression RPAREN
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_postfix_expression(p):
  '''postfix_expression : primary_expression
	| postfix_expression LSQUAREBRACKET expression RSQUAREBRACKET
	| postfix_expression LPAREN RPAREN
  | postfix_expression LPAREN argument_expression_list RPAREN
  | postfix_expression PERIOD ID
	| postfix_expression ARROW ID
	| postfix_expression INCREMENT
	| postfix_expression DECREMENT
  '''  
  #p[0] = Node()
  p[0] = build_AST(p)

def p_argument_expression_list(p):
  '''argument_expression_list : assignment_expression
                              | argument_expression_list COMMA assignment_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)
  # if(len(p) == 2):
  #   p[0] = p[1]
  # else:
  #   p[1].append(p[3])
  #   p[0] = p[1]

def p_unary_expression(p):
  '''unary_expression : postfix_expression
                      | INCREMENT unary_expression
                      | DECREMENT unary_expression
                      | unary_operator cast_expression
                      | SIZEOF unary_expression
                      | SIZEOF LPAREN type_name RPAREN
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_unary_operator(p):
  '''unary_operator : AND
                    | MULTIPLY
                    | PLUS
                    | MINUS
                    | NOT
                    | LNOT
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_cast_expression(p):
  '''cast_expression : unary_expression
                     | LPAREN type_name RPAREN cast_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_multipicative_expression(p):
  '''multiplicative_expression : cast_expression
	| multiplicative_expression MULTIPLY cast_expression
	| multiplicative_expression DIVIDE cast_expression
	| multiplicative_expression MOD cast_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_additive_expression(p):
  '''additive_expression : multiplicative_expression
	| additive_expression PLUS multiplicative_expression
	| additive_expression MINUS multiplicative_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_shift_expression(p):
  '''shift_expression : additive_expression
	| shift_expression LSHIFT additive_expression
	| shift_expression RSHIFT additive_expression
	'''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_relational_expression(p):
  '''relational_expression : shift_expression
	| relational_expression LESS shift_expression
	| relational_expression GREATER shift_expression
	| relational_expression LESSEQUAL shift_expression
	| relational_expression GREATEREQUAL shift_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_equality_expresssion(p):
  '''equality_expression : relational_expression
	| equality_expression EQUAL relational_expression
	| equality_expression NOTEQUAL relational_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_and_expression(p):
  '''and_expression : equality_expression
	| and_expression AND equality_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_exclusive_or_expression(p):
  '''exclusive_or_expression : and_expression
	| exclusive_or_expression XOR and_expression
	'''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_inclusive_or_expression(p):
  '''inclusive_or_expression : exclusive_or_expression
	| inclusive_or_expression OR exclusive_or_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_logical_and_expression(p):
  '''logical_and_expression : inclusive_or_expression 
  | logical_and_expression LAND inclusive_or_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_logical_or_expression(p):
  '''logical_or_expression : logical_and_expression
	| logical_or_expression LOR logical_and_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_conditional_expression(p):
  '''conditional_expression : logical_or_expression
	| logical_or_expression CONDOP expression COLON conditional_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_assignment_expression(p):
  '''assignment_expression : conditional_expression 
  | unary_expression assignment_operator assignment_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

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
  p[0] = build_AST(p)

def p_expression(p):
  '''expression : assignment_expression
	| expression COMMA assignment_expression
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_constant_expression(p):
  '''constant_expression : conditional_expression'''
  p[0] = build_AST(p)

def p_declaration(p):
  '''declaration : declaration_specifiers SEMICOLON
	| declaration_specifiers init_declarator_list SEMICOLON
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_declaration_specifiers(p):
  '''declaration_specifiers : storage_class_specifier
	| storage_class_specifier declaration_specifiers
	| type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_init_declarator_list(p):
  '''init_declarator_list : init_declarator
	| init_declarator_list COMMA init_declarator
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_init_declarator(p):
  '''init_declarator : declarator
	| declarator EQUALS initializer
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_storage_class_specifier(p):
  '''storage_class_specifier : TYPEDEF
	| EXTERN
	| STATIC
	| AUTO
	| REGISTER
  '''
  #p[0] = Node()
  p[0] = build_AST(p)



def p_type_specifier(p):
  '''type_specifier : VOID
                    | CHAR
                    | SHORT
                    | INT
                    | LONG
                    | FLOAT
                    | DOUBLE
                    | SIGNED
                    | UNSIGNED
                    | struct_or_union_specifier
                    | enum_specifier
                    | TYPE_NAME
  '''
  #p[0] = Node()
  p[0] = build_AST(p)

def p_struct_or_union_specifier(p):
  '''struct_or_union_specifier : struct_or_union ID LCURLYBRACKET struct_declaration_list RCURLYBRACKET
  | struct_or_union LCURLYBRACKET struct_declaration_list RCURLYBRACKET
  | struct_or_union ID
  '''
  p[0] = build_AST(p)

def p_struct_or_union(p):
  '''struct_or_union : STRUCT
	| UNION
  '''
  p[0] = build_AST(p)

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
  '''enum_specifier : ENUM LCURLYBRACKET enumerator_list RCURLYBRACKET
	| ENUM ID LCURLYBRACKET enumerator_list RCURLYBRACKET
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
                   | LCURLYBRACKET initializer_list RCURLYBRACKET
                   | LCURLYBRACKET initializer_list COMMA RCURLYBRACKET                                   
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
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_labeled_statement(p):
    '''labeled_statement : ID COLON statement 
                         | CASE constant_expression COLON statement
                         | DEFAULT COLON statement
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_compound_statement(p):
    '''compound_statement : LCURLYBRACKET RCURLYBRACKET
                          | LCURLYBRACKET statement_list RCURLYBRACKET
                          | LCURLYBRACKET declaration_list RCURLYBRACKET
                          | LCURLYBRACKET declaration_list statement_list RCURLYBRACKET
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
    '''selection_statement : IF LPAREN expression RPAREN statement
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
    p[0] = build_AST(p)

def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration
    '''
    #p[0] = Node()
    p[0] = build_AST(p)

def p_function_definition(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement
                           | declaration_specifiers declarator compound_statement
                           | declarator declaration_list compound_statement
                           | declarator compound_statement                                                                              
    ''' 
    #p[0] = Node()
    p[0] = build_AST(p)                       

# Error rule for syntax errors
def p_error(p):
    # print(p)
    print("Syntax error in input!")
    # p.lineno(1)

def runmain(code):
  open('graph1.dot','w').write("digraph ethane {")
  parser = yacc.yacc(start = 'translation_unit')
  result = parser.parse(code,debug = False)
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
