import re
import ply.lex as lex

keyword_tokens = {}

keywords = ('AUTO', 'BREAK', 'CASE', 'CHAR', 'CONST','CONTINUE',
'DEFAULT', 'DO', 'DOUBLE', 'ELSE', 'ENUM', 'EXTERN',
'FLOAT', 'FOR', 'GOTO', 'IF', 'INT', 'LONG','REGISTER', 
'RETURN', 'SHORT', 'SIGNED', 'SIZEOF', 'STATIC', 'STRUCT',
'SWITCH', 'TYPEDEF', 'UNION', 'UNSIGNED', 'VOID','VOLATILE', 'WHILE')


tokens = keywords + ('ID',
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

'COMMA', 'SEMICOLON', 'COLON', 'PERIOD', 'HASH' # , ; : . #

# various brackets 
'LPAREN', 'RPAREN',
'LSQUAREBRACKET', 'RSQUAREBRACKET',
'LCURLYBRACKET', 'RCURLYBRACKET',
)


for s in keywords:
    low_s = s.lower()
    keyword_tokens[low_s] = s

# print(tokens)

t_identifier = r'[a-zA-Z_][a-zA-Z0-9_]*'


