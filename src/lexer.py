import re
import ply.lex as lex
from ply.lex import TOKEN

keyword_tokens = {}

keywords = ('AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST','CONTINUE',
'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN',
'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG','REGISTER', 
'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT',
'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID','VOLATILE', 'WHILE')


tokens = keywords + ('ID','CHAR_CONST', 'INT_CONST', 'STRING_LITERAL',
# operators
'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MOD', # + - * / %
'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
'LOR', 'LAND', 'LNOT',
'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 'EQUAL', 'NOTEQUAL',

# assignment statements
'PLUSEQUAL', 'MINUSEQUAL',
'EQUALS', 'MULTIPLYEQUAL', 'DIVIDEEQUAL', 'MODEQUAL',
'LSHIFTEQUAL','RSHIFTEQUAL', 'ANDEQUAL', 'XOREQUAL',
'OREQUAL',

# unary operators
'INCREMENT', 'DECREMENT',

# comma etc.

'COMMA', 'SEMICOLON', 'COLON', 'PERIOD', 'HASH', 'ELLIPSIS', # , ; : . ...#

# various brackets 
'LPAREN', 'RPAREN',
'LSQUAREBRACKET', 'RSQUAREBRACKET',
'LCURLYBRACKET', 'RCURLYBRACKET',
)


for s in keywords:
    low_s = s.lower()
    keyword_tokens[low_s] = s

t_PLUS              = r'\+'
t_MINUS             = r'-'
t_MULTIPLY             = r'\*'
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

# Assignment operators
t_EQUALS            = r'='
t_MULTIPLYEQUAL        = r'\*='
t_DIVIDEEQUAL          = r'/='
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
t_HASH              = r'\#'


def t_INT_CONST(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CHAR_CONST(t):
    r'\'(\\.|[^\\\'])+\''
    return t

def t_STRING_LITERAL(t):
    r'\"(\\.|[^\\"])*\"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keyword_tokens.get(t.value,'ID')    # Check for reserved words
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# lexer = lex.lex()

# # Test it out
# data = '''
# char x = 'xyx'
# '''

# # Give the lexer some input
# lexer.input(data)

# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break      # No more input
#     print(tok)


