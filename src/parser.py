# Yacc example

import ply.yacc as yacc


# left for now
# postfix_expression

# Get the token map from the lexer.  This is required.
from lexer import tokens

precedence = (
        ('left', 'LOR'),
        ('left', 'LAND'),
        ('left', 'OR'),
        ('left', 'XOR'),
        ('left', 'AND'),
        ('left', 'EQUAL', 'NOTEQUAL'),
        ('left', 'GREATER', 'GREATEREQUAL', 'LESS', 'LESSEQUAL'),
        ('left', 'RSHIFT', 'LSHIFT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'MOD')
    )


def p_primary_expression(p):
  '''primary_expression : ID
                | INT_CONST
                | FLOAT_CONST
                | CHAR_CONST
                | STRING_LITERAL
                | LPAREN expression RPAREN
  '''
  if(len(p) == 2):
    p[0] = p[1]
  else:  
    p[0] = p[2]

def p_argument_expression_list(p):
  '''argument_expression_list : assignment_expression
                              | argument_expression_list COMMA assignment_expression
  '''
  if(len(p) == 2):
    p[0] = p[1]
  else:
    p[1].exprs.append(p[3])
    p[0] = p[1]


def p_postfix_expression(p):
  '''postfix_expression : primary_expression
	| postfix_expression LSQUAREBRACKET expression RSQUAREBRACKET
	| postfix_expression LPAREN RPAREN
  | postfix_expression PERIOD ID
	| postfix_expression LPAREN argument_expression_list RPAREN
	| postfix_expression ARROW ID
	| postfix_expression INCREMENT
	| postfix_expression DECREMENT
  '''  

def p_unary_expression(p):
  '''unary_expression : postfix_expression
                      | INCREMENT unary_expression
                      | DECREMENT unary_expression
                      | unary_operator cast_expression
                      | SIZEOF unary_expression
                      | SIZEOF LPAREN type_name RPAREN
  '''

def p_unary_operator(p):
  '''unary_operator : AND
                    | MULTIPLY
                    | PLUS
                    | MINUS
                    | NOT
                    | LNOT
  '''

def p_cast_expression(p):
  '''cast_expression : unary_expression
                     | LPAREN type_name RPAREN cast_expression
  '''

def p_multipicative_expression(p):
  '''multiplicative_expression : cast_expression
	| multiplicative_expression MULTIPLY cast_expression
	| multiplicative_expression DIVIDE cast_expression
	| multiplicative_expression MOD cast_expression
  '''

def p_additive_expression(p):
  '''additive_expression : multiplicative_expression
	| additive_expression PLUS multiplicative_expression
	| additive_expression MINUS multiplicative_expression
  '''

def p_shift_expression(p):
  '''shift_expression : additive_expression
	| shift_expression LSHIFT additive_expression
	| shift_expression RSHIFT additive_expression
	'''

def p_relational_expression(p):
  '''relational_expression : shift_expression
	| relational_expression LESS shift_expression
	| relational_expression GREATER shift_expression
	| relational_expression LESSEQUAL shift_expression
	| relational_expression GREATEREQUAL shift_expression
  '''

def p_equality_expresssion(p):
  '''equality_expression : relational_expression
	| equality_expression EQUAL relational_expression
	| equality_expression NOTEQUAL relational_expression
  '''

def p_and_expression(p):
  '''and_expression : equality_expression
	| and_expression AND equality_expression
  '''

def p_exclusive_or_expression(p):
  '''exclusive_or_expression : and_expression
	| exclusive_or_expression XOR and_expression
	'''

def p_inclusive_or_expression(p):
  '''inclusive_or_expression : exclusive_or_expression
	| inclusive_or_expression OR exclusive_or_expression
  '''

def p_logical_and_expression(p):
  '''logical_and_expression : inclusive_or_expression 
  | logical_and_expression LAND inclusive_or_expression
  '''

def p_logical_or_expression(p):
  '''logical_or_expression : logical_and_expression
	| logical_or_expression LOR logical_and_expression
  '''

def p_conditional_expression(p):
  '''conditional_expression : logical_or_expression
	| logical_or_expression CONDOP expression COLON conditional_expression
  '''

def p_assignment_expression(p):
  '''assignment_expression : conditional_expression 
  | unary_expression assignment_operator assignment_expression
  '''

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

def p_expression(p):
  '''expression : assignment_expression
	| expression COMMA assignment_expression
  '''

def p_constant_expression(p):
  '''constant_expression : conditional_expression'''

def p_declaration(p):
  '''declaration : declaration_specifiers SEMICOLON
	| declaration_specifiers init_declarator_list SEMICOLON
  '''

def p_declaration_specifiers(p):
  '''declaration_specifiers : storage_class_specifier
	| storage_class_specifier declaration_specifiers
	| type_specifier
	| type_specifier declaration_specifiers
	| type_qualifier
	| type_qualifier declaration_specifiers
  '''

def p_init_declarator_list(p):
  '''init_declarator_list : init_declarator
	| init_declarator_list COMMA init_declarator
  '''
def p_init_declarator(p):
  '''init_declarator : declarator
	| declarator EQUALS initializer
  '''

def p_storage_class_specifier(p):
  '''storage_class_specifier : TYPEDEF
	| EXTERN
	| STATIC
	| AUTO
	| REGISTER
  '''

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
                     | type_name
    '''

def p_specifier_qualifier_list(p):
  '''specifier_qualifier_list : type_specifier specifier_qualifier_list
  | type_specifier
  | type_qualifier specifier_qualifier_list
  | type_qualifier
  '''

def p_type_qualifier(p):
    '''type_qualifier : CONST
                      | VOLATILE
    '''
    p[0] = p[1]

def p_declarator(p):
  '''declarator : pointer direct_declarator
  | direct_declarator
  '''

def p_direct_declarator(p):
    '''direct_declarator : ID
                         | LPAREN declarator RPAREN
                         | direct_declarator LSQUAREBRACKET constant_expression RSQUAREBRACKET
                         | direct_declarator LSQUAREBRACKET RSQUAREBRACKET
                         | direct_declarator LPAREN parameter_type_list RPAREN
                         | direct_declarator LPAREN identifier_list RPAREN
                         | direct_declarator LPAREN RPAREN
    '''

def p_type_qualifier_list(p):
    '''type_qualifier_list : type_qualifier
                          | type_qualifier_list type_qualifier
    '''
def p_pointer(p):
    '''pointer : MULTIPLY 
               | MULTIPLY type_qualifier_list
               | MULTIPLY type_qualifier_list pointer
               | MULTIPLY pointer
    '''


def p_parameter_type_list(p):
    '''parameter_type_list : parameter_list
                           | parameter_list COMMA ELLIPSIS
    '''

def p_parameter_list(p):
    '''parameter_list : parameter_declaration
                      | parameter_list COMMA parameter_declaration
    '''

def p_parameter_declaration(p):
    '''parameter_declaration : declaration_specifiers declarator
                             | declaration_specifiers abstract_declarator
                             | declaration_specifiers
    '''

def p_identifier_list(p):
    '''identifier_list : ID
                       | identifier_list COMMA ID
    '''

def p_type_name(p):
    '''type_name : specifier_qualifier_list
                 | specifier_qualifier_list abstract_declarator
    '''

def p_abstract_declarator(p):
    '''abstract_declarator : pointer 
                           | direct_abstract_declarator
                           | pointer direct_abstract_declarator
    '''

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

def p_initializer(p):
    '''initializer : assignment_expression
                   | LCURLYBRACKET initializer_list RCURLYBRACKET
                   | LCURLYBRACKET initializer_list COMMA RCURLYBRACKET                                   
    '''

def p_initializer_list(p):
  '''initializer_list : initializer
  | initializer_list COMMA initializer
  '''

def p_statement(p):
    '''statement : labeled_statement
                 | compound_statement
                 | expression_statement
                 | selection_statement
                 | iteration_statement
                 | jump_statement
    '''

def p_labeled_statement(p):
    '''labeled_statement : ID COLON statement 
                         | CASE constant_expression COLON statement
                         | DEFAULT COLON statement
    '''

def p_compound_statement(p):
    '''compound_statement : LCURLYBRACKET RCURLYBRACKET
                          | LCURLYBRACKET statement_list RCURLYBRACKET
                          | LCURLYBRACKET declaration_list RCURLYBRACKET
                          | LCURLYBRACKET declaration_list statement_list RCURLYBRACKET
    '''                          

def p_expression_statement(p):
    '''expression_statement : SEMICOLON
                            | expression SEMICOLON
    '''

def p_declaration_list(p):
    '''declaration_list : declaration
                        | declaration_list declaration
    '''

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement
    '''

def p_selection_statement(p):
    '''selection_statement : IF LPAREN expression RPAREN statement
                           | IF LPAREN expression RPAREN statement ELSE statement
                           | SWITCH LPAREN expression RPAREN statement
    '''

def p_iteration_statement(p):
    '''iteration_statement : WHILE LPAREN expression RPAREN
                           | DO statement WHILE LPAREN expression RPAREN SEMICOLON
                           | FOR LPAREN expression_statement expression_statement RPAREN statement
                           | FOR LPAREN expression_statement expression_statement expression RPAREN statement                                                 
    '''

def p_jump_statement(p):
    '''jump_statement : GOTO ID SEMICOLON
                      | CONTINUE SEMICOLON
                      | BREAK SEMICOLON
                      | RETURN SEMICOLON
                      | RETURN expression SEMICOLON
    '''

def p_translation_unit(p):
    '''translation_unit : external_declaration
                        | translation_unit external_declaration
    '''

def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration
    '''

def p_function_definition(p):
    '''function_definition : declaration_specifiers declarator declaration_list compound_statement
                           | declaration_specifiers declarator compound_statement
                           | declarator declaration_list compound_statement
                           | declarator compound_statement                                                                              
    '''                        

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
# parser = yacc.yacc(start = 'translation_unit')
# while True:
#   try:
#     s = input('calc > ')
#   except EOFError:
#     break
#   # z = code.readlines()
#   if not s: continue
#   print(s)
#   result = parser.parse(s,debug=True)
#   print(result)
def runmain(code):
  parser = yacc.yacc(start = 'translation_unit')
  for line in code.splitlines():
    print(line)
    if not line: continue
    result = parser.parse(line,debug = False)
    print(result)
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