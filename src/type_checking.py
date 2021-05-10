import lexer
class Node:
  def __init__(self,name = '',val = '',lno = 0,type = '',children = '',scope = 0, array = [], maxDepth = 0,isFunc = 0,
    parentStruct = '', level = 0,ast = None, place = None, quad = None, expr = [], label = [], tind = '', addr = '', sqb = False):
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
    self.place = place
    self.quad = quad
    self.expr = expr
    self.label = label
    self.tind = tind
    self.addr = addr
    self.sqb = sqb
    if children:
      self.children = children
    else:
      self.children = []

def give_error():
  global syn_error_count
  lexer.syn_error_count = lexer.syn_error_count+1 

def int_or_real(dtype):
  arr = dtype.split()
  if ('*' in arr):
    return 'int'
  if 'long' in arr:
    return 'int' 
  elif ( ('int' in arr) or ('char' in arr) or ('short' in arr) ):
    return 'int'
  else:
    return 'int'

def extract_if_tuple(p2):
  if (type(p2) is tuple):
    return str(p2[0])
  else:
    return str(p2)

def get_higher_data_type(type_1 , type_2):
  if (type_1 == '' or type_2 == ''):
    return ''
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

def check_func_call_op(func_argument,call_argument,i,lno):
    if(func_argument == call_argument):
        return
    # if(func_argument)
    if(func_argument in ['int','float','char']):
        if(call_argument in ['int','char','float']):
            return
        print("error at line " + str(lno), ": Type mismatch in argument " + str(i+1) + " of function call, " + 'actual type : ' + func_argument + ', called with : ' + call_argument)
        give_error()
    elif(func_argument.endswith('*')):
        if(not call_argument.endswith('*')):
            print("error at line " + str(lno), ": Type mismatch in argument " + str(i+1) + " of function call, " + 'actual type : ' + func_argument + ', called with : ' + call_argument)
            give_error()
        else:
            print("warning at line " + str(lno), ": Implicit pointer convrsion during function call")
    else:
        print("error at line " + str(lno), ": Type mismatch in argument " + str(i+1) + " of function call, " + 'actual type : ' + func_argument + ', called with : ' + call_argument)   
        give_error()  

def check_func_return_type(expression_type,func_return_type,lno):
  print(expression_type,func_return_type,lno)
  if(expression_type in ['int','char','float'] and func_return_type in ['int','char','float']):
    return
  if(expression_type == func_return_type):
    return
  if(expression_type == ''):
    return
  if(func_return_type == 'void'):
    print('error at line ' + str(lno) + ": function with return type void cannot return a value")
    give_error()
  elif(func_return_type.endswith('*')):
    if(not expression_type.endswith('*')):
      print('error at line ' + str(lno) + ': function return type is not ' + expression_type)
      give_error()
    else:
      print('warning at line ' + str(lno) + ' implicit pointer conversion')
  else:
    print('error at line ' + str(lno) + ': function return type is not ' + expression_type)
    give_error()

