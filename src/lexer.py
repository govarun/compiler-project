import re
import ply.lex as lex
from ply.lex import TOKEN
from tabulate import tabulate

keyword_tokens = {}
keywords = {'auto':'AUTO', 'break':'BREAK', 'case':'CASE', 'char':'CHAR', 'const':'CONST','continue':'CONTINUE',
'default':'DEFAULT', 'do':'DO', 'double':'DOUBLE', 'else':'ELSE', 'enum':'ENUM', 'extern':'EXTERN',
'float':'FLOAT', 'for':'FOR', 'goto':'GOTO', 'if':'IF', 'int':'INT', 'long':'LONG','register':'REGISTER', 
'return':'RETURN', 'short':'SHORT', 'signed':'SIGNED', 'sizeof':'SIZEOF', 'static':'STATIC', 'struct':'STRUCT',
'switch':'SWITCH', 'typedef':'TYPEDEF', 'union':'UNION', 'unsigned':'UNSIGNED', 'void':'VOID', 'volatile':'VOLATILE', 
'while':'WHILE', 'type_name':'TYPE_NAME'}


tokens = ['ID','CHAR_CONST', 'INT_CONST', 'FLOAT_CONST', 'STRING_LITERAL', 'OCTAL_CONST', 'HEX_CONST', 'BIN_CONST',
# operators
'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MOD', # + - * / %
'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
'LOR', 'LAND', 'LNOT',
'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 'EQUAL', 'NOTEQUAL',
                     
# Structure dereference (->)
'ARROW',

# Conditional operator (?)
'CONDOP',                     

# assignment statements
'PLUSEQUAL', 'MINUSEQUAL',
'EQUALS', 'MULTIPLYEQUAL', 'DIVIDEEQUAL', 'MODEQUAL',
'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
'OREQUAL',

# unary operators
'INCREMENT', 'DECREMENT',

# comma etc.

'COMMA', 'SEMICOLON', 'COLON', 'PERIOD', 'ELLIPSIS', # , ; : . ...#

# various brackets 
'LPAREN', 'RPAREN',
'LSQUAREBRACKET', 'RSQUAREBRACKET',
'LCURLYBRACKET', 'RCURLYBRACKET',
] + list(keywords.values())

literals = [';', '(']

# for s in keywords:
#     low_s = s.lower()
#     keyword_tokens[low_s] = s

t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULTIPLY          = r'\*'
t_DIVIDE            = r'/'
t_MOD               = r'%'
t_OR                = r'\|'
t_AND               = r'&'
t_NOT               = r'~'
t_XOR               = r'\^'
t_LSHIFT            = r'<<'
t_RSHIFT            = r'>>'
t_LOR               = r'\|\|'
t_LAND              = r'&&'
t_LNOT              = r'!'
t_LESS              = r'<'
t_GREATER           = r'>'
t_LESSEQUAL         = r'<='
t_GREATEREQUAL      = r'>='
t_EQUAL             = r'=='
t_NOTEQUAL          = r'!='
t_ARROW             = r'->'
t_CONDOP            = r'\?'


# Assignment operators
t_EQUALS            = r'='
t_MULTIPLYEQUAL     = r'\*='
t_DIVIDEEQUAL       = r'/='
t_MODEQUAL          = r'%='
t_PLUSEQUAL         = r'\+='
t_MINUSEQUAL        = r'-='
t_LSHIFTEQUAL       = r'<<='
t_RSHIFTEQUAL       = r'>>='
t_ANDEQUAL          = r'&='
t_OREQUAL           = r'\|='
t_XOREQUAL          = r'\^='

# Increment/decrement
t_INCREMENT         = r'\+\+'
t_DECREMENT         = r'--'

# Delimeters
t_LPAREN            = r'\('
t_RPAREN            = r'\)'
t_LSQUAREBRACKET     = r'\['
t_RSQUAREBRACKET    = r'\]'
t_COMMA             = r','
t_PERIOD            = r'\.'
t_SEMICOLON         = r';'
t_COLON             = r':'
t_ELLIPSIS          = r'\.\.\.'
t_LCURLYBRACKET     = r'\{'
t_RCURLYBRACKET     = r'\}'


integer_suffix_opt = r'(([uU]ll)|([uU]LL)|(ll[uU]?)|(LL[uU]?)|([uU][lL])|([lL][uU]?)|[uU])?'
decimal_constant = '(0'+integer_suffix_opt+')|([1-9][0-9]*'+integer_suffix_opt+')'


def t_FLOAT_CONST(t):
    r'[0-9]*([.][0-9]+)?([eE][+-]?[0-9]+) | ([0-9]*[.])[0-9]+'
    t.value = t.value
    return t
  
def t_HEX_CONST(t):
    r'0[xX][0-9a-fA-F]+'
    # t.value = int(t.value,16)
    return t

def t_BIN_CONST(t):
    r'0b[01]+'
    return t

def t_OCTAL_CONST(t):
    r'0[0-7]+'
    # t.value = int(t.value,8)
    return t

# def t_INV_OCTAL(t):
#     r'0[0-9]+'
#     col_number = find_column(code_string, t)
#     formatted_error = "Invalid octal number \'{character}\' at lineno {lineno} at position {colno}".format(character=t.value, lineno=t.lineno, colno=str(col_number))
#     # print("Illegal character '%s' at line " % t.value[0])
#     print(formatted_error)
#     t.lexer.skip(1)

@TOKEN(decimal_constant)
def t_INT_CONST(t):
    # r'0|[1-9][0-9]*'
    # t.value = int(t.value)
    # print(t.type)
    return t

def t_CHAR_CONST(t):
    r'\'(\\.|[^\\\'])+\''
    return t

def t_STRING_LITERAL(t):
    r'\"(\\.|[^\\"])*\"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value,'ID')    # Check for reserved words
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    
def t_COMMENT(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/|//.*'
    for c in t.value:
        if c == '\n':
            t.lexer.lineno += 1
    pass

t_ignore  = ' \t\v\f'


def find_column(code,token):
    line_start = code.rfind('\n',0,token.lexpos) + 1
    # print(token.lexpos)
    return (token.lexpos - line_start) + 1

def t_error(t):
    col_number = find_column(code_string,t)
    formatted_error = "Illegal character \'{character}\' at lineno {lineno} at position {colno}".format(character = t.value[0],lineno = t.lineno,colno = str(col_number))
    # print("Illegal character '%s' at line " % t.value[0])
    print(formatted_error)
    t.lexer.skip(1)

lexer = lex.lex(debug=False)
# def runmain(code):
#     global code_string
#     code_string = code
#     lexer = lex.lex(debug=False)
#     lexer.input(code)
#     # Tokenize

#     formatted_output = []
#     # print("Token      Lexeme      Line#     Column#")
#     heading = ["Token","Lexeme","Line#","Column#"]
#     formatted_output.append(heading)
    
#     while True:
#         tok = lexer.token()
#         if not tok:
#             break      # No more input
#         col_number = find_column(code,tok)
#         temp_row = [str(tok.type),str(tok.value),str(tok.lineno),str(col_number)]
#         # print(tok.type, tok.value, tok.lineno, col_number)
#         formatted_output.append(temp_row)
    
#     print(tabulate(formatted_output))



