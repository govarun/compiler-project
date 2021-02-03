# all the tokens that have to be identified by the lexer
## all the required keywords - 
# "auto"		
# "break"			
# "case"		
# "char"		
# "const"			
# "continue"		
# "default"	
# "do"
# "double"		
# "else"		
# "enum"		
# "extern"		
# "float"			
# "for"	
# "goto"		
# "if"
# "int"	
# "long"		
# "register"		
# "return"		
# "short"			
# "signed"		
# "sizeof"		
# "static"		
# "struct"		
# "switch"		
# "typedef"		
# "union"			
# "unsigned"		
# "void"		
# "volatile"		
# "while"
class TokenType:
    def __init__(self,name,listName):
        self.name = name
        listName.append(self)
    def token_name(self):
        return self.name


keywords = []
AUTO = TokenType("auto",keywords)
BREAK = TokenType("break",keywords) 
CASE = TokenType("case",keywords)
CHAR  = TokenType("char",keywords)
CONST = TokenType("const",keywords)
CONTINUE = TokenType("continue",keywords)
DEFAULT = TokenType("default",keywords)
DO = TokenType("do",keywords)
DOUBLE = TokenType("double",keywords)
ELSE = TokenType("else",keywords)
ENUM = TokenType("enum",keywords)
EXTERN = TokenType("extern",keywords)
FLOAT = TokenType("float",keywords)
FOR = TokenType("for",keywords)
GOTO = TokenType("goto",keywords)
IF = TokenType("if",keywords)
INT = TokenType("int",keywords)
LONG = TokenType("long",keywords)
REGISTER = TokenType("register",keywords)
RETURN = TokenType("return",keywords)
SHORT = TokenType("short",keywords)
SIGNED = TokenType("signed",keywords)
SIZEOF = TokenType("sizeof",keywords)
STATIC = TokenType("static",keywords)
STRUCT = TokenType("struct",keywords)
SWITCH = TokenType("switch",keywords)
TYPEDEF = TokenType("typedef",keywords)
UNION = TokenType("union",keywords)
UNSIGNED = TokenType("unsigned",keywords)
VOID = TokenType("void",keywords)
VOLATILE = TokenType("volatile",keywords)
WHILE = TokenType("while",keywords)

