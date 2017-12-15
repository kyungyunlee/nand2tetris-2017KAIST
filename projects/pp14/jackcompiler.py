#
# Compile Jack source to VM
#

import tokens
import jackparser
from parsetree import *
import sys, os

# --------------------------------------------------------------------

binopmap = { "+" : "add",
             "-" : "sub",
             "*" : "call Math.multiply 2",
             "/" : "call Math.divide 2",
             "&" : "and",
             "|" : "or",
             ">" : "gt",
             "<" : "lt",
             "=" : "eq" }
  
# --------------------------------------------------------------------

class JackCompiler():
  def __init__(self, folder, tokenizer):
    self.folder = folder
    self.temp_count = 0
    self.local_count = 0
    self.while_count = 1
    self.if_count = 1

  # ------------------------------------------------------------------
    
  def compile(self, jclass):
    "Compile one class."
    sys.stderr.write("Compiling %s ...\n" % jclass.name)
    self.out = open("%s/%s.vm" % (self.folder, jclass.name), "w")
    self.out.write("// class %s\n" % jclass.name)
    for sb in jclass.subroutines:
      self.out.write("// %s %s %s.%s\n" %
                     (sb.kind, sb.ret_type, jclass.name, sb.name))
      self.compile_subroutine(jclass, sb)
    self.out.close()

  def compile_subroutine(self, jclass, sb):
    self.out.write("function %s.%s %d\n" %
                   (jclass.name, sb.name, len(sb.locals)))
    # some more work is needed here for methods and constructors
    # add all the local variables to the jclass.fields
    for i in range(len(sb.locals)):
      if sb.locals[i][0] not in [e[0] for e in jclass.fields] :
        jclass.addvars("field", sb.locals[i][1], [elem[0] for elem in sb.locals])

    for st in sb.statements:
      self.compile_statement(jclass, sb, st)

  def compile_statement(self, jclass, sb, st):
    if isinstance(st, LetStatement):
      self.compile_let(jclass, sb, st)
    if isinstance(st, CallExpression):
      self.compile_do(jclass, sb, st)
    if isinstance(st, IfStatement):
      self.compile_if(jclass, sb, st)
    if isinstance(st, WhileStatement):
      self.compile_while(jclass, sb, st)
    if isinstance(st, ReturnStatement):
      self.compile_return(jclass, sb, st)

  # ------------------------------------------------------------------

  #
  # In all compile_xxx methods, jclass is a JackClass object
  # describing the class containing the code being compiled, and
  # sb is a Subroutine object describing the function/method/constructor.
  # 

  # let is of type LetStatement
  def compile_let(self, jclass, sb, let):
    is_found_local = False
    is_found_arg = False
    local = 0
    temp1 = ""
    is_array = False


    temp = -1
    if (len(sb.locals)>0):
      for i in range(len(sb.locals)):
        if sb.locals[i][0] == let.vname:
          temp = i
          is_found_local = True

    if not is_found_local:
      for i in range(len(sb.arguments)):
        if sb.arguments[i][0] == let.vname:
          temp = i
          is_found_arg = True

    # if there is index
    if (let.index != None):
      is_array = True
      self.compile_expression(jclass,sb, let.index)
      if is_found_local:
        self.out.write("push %s %d\n" %("local", temp))
      elif is_found_arg:
        self.out.write("push argument %d\n"%temp)
      self.out.write("add\n")

    # right
    self.compile_expression(jclass,sb, let.expr)


    # calculate pointer
    if (is_array):
      self.out.write("pop temp %d\n"%0)
      self.out.write("pop pointer %d\n"%1)
      self.out.write("push temp %d\n"%0)
      self.out.write("pop that %d\n"%0)

    else :
      #self.out.write("wh..push local %d\n" % temp)
      if is_found_local:
        self.out.write("pop local %d\n" % temp)
      elif is_found_arg:
        self.out.write("pop argument %d\n"%temp)


  # st is of type CallExpression
  def compile_do(self, jclass, sb, st):
    self.compile_call(jclass, sb, st)
    self.out.write("pop temp 0 // void\n")

  # ifst is of type IfStatement
  def compile_if(self, jclass, sb, ifst):
    self.compile_expression(jclass, sb, ifst.expr)
    self.out.write("not\n")
    #self.if_count +=1
    #temp = self.if_count
    self.out.write("if-goto IF.%d\n"% self.if_count)

    if (ifst.if_statements != None):
      self.compile_statement(jclass, sb, ifst.if_statements[0])
      #self.if_count += 1
      self.out.write("goto IF.%d\n"%(self.if_count+1)) # skip else and go beyond else
    self.out.write("label IF.%d\n" % (self.if_count)) # else statement
    if (ifst.else_statements != None):
      self.compile_statement(jclass, sb, ifst.else_statements[0])
    self.out.write("label IF.%d\n"%(self.if_count+1)) # after if else statement
    self.if_count+=1

  # whilest is of type WhileStatement
  def compile_while(self, jclass, sb, whilest):
    self.out.write("label WHILE.%d\n" % self.while_count)
    self.while_count +=1

    self.compile_expression(jclass, sb ,whilest.expr)
    self.out.write("not\n")
    self.out.write("if-goto WHILE.%d\n" %self.while_count) # exit?
    for i in range(len(whilest.statements)):
        self.compile_statement(jclass, sb, whilest.statements[i])
    self.out.write("goto WHILE.%d\n" % (self.while_count-1))
    self.out.write("label WHILE.%d\n" % self.while_count)
    self.while_count +=1



  # st is of type ReturnStatement
  def compile_return(self, jclass, sb, st):
    if st.expr is None:
      self.out.write("push constant 0\n")
    else:
      self.compile_expression(jclass, sb, st.expr)
    self.out.write("return\n")
    
  # ------------------------------------------------------------------

  #
  # expr is an expression, and can be of type int, str (for string
  # literals), ConstantExpression, VariableExpression, UnaryOperation,
  # BinaryOperation, or CallExpression.
  #
  
  def compile_expression(self, jclass, sb, expr):
    if isinstance(expr, int):
      self.out.write("push constant %d\n" % expr)
    if isinstance(expr, str):
      self.compile_literal(expr)
    if isinstance(expr, ConstantExpression):
      self.compile_constant(expr)
    if isinstance(expr, VariableExpression):
      self.compile_variable(jclass, sb, expr)
    if isinstance(expr, CallExpression):
      self.compile_call(jclass, sb, expr)
    if isinstance(expr, BinaryOperation):
      self.compile_binaryop(jclass, sb, expr)
    if isinstance(expr, UnaryOperation):
      self.compile_unaryop(jclass, sb, expr)

  def compile_constant(self, expr):
    if expr.value == "this":
      self.out.write("push pointer 0 // this\n")
    else:
      self.out.write("push constant 0 // %s\n" % expr.value)
      if expr.value == "true":
        self.out.write("not\n")  # true is -1
    
  def compile_literal(self, text):
    self.out.write('push constant %d // "%s"\n' % (len(text), text))
    self.out.write("call String.new 1\n")
    for ch in text:
      self.out.write("push constant %d // '%s'\n" % (ord(ch), ch))
      self.out.write("call String.appendChar 2\n")

  # var is of type VariableExpression
  def compile_variable(self, jclass, sb, var):
      temp = -1
      is_found_local = False
      is_found_arg = False
      if (len(sb.locals)>0):
        for i in range(len(sb.locals)):
          if sb.locals[i][0] == var.name:
            temp = i
            is_found_local = True
      if not is_found_local:
        if (len(sb.arguments) > 0):
          for i in range(len(sb.arguments)):
            if sb.arguments[i][0] == var.name:
              temp = i
              is_found_arg = True

      if is_found_local:
        self.out.write("push local %d\n" % temp)
      elif is_found_arg:
        self.out.write("push argument %d\n" %temp)

      if not var.index == None:
        self.compile_expression(jclass, sb, var.index)
        self.out.write("add\n")
        self.out.write("pop pointer 1\n")
        self.out.write("push that 0\n")

  # call is of type CallExpression
  def compile_call(self, jclass, sb, call):
    arguments = call.arguments # type : parsetree.BinaryOperat
    # add local variables to the jack class function
    for j in range(len(arguments)):
      self.compile_expression(jclass,sb, arguments[j])
    self.out.write("call %s.%s %d\n" % (call.container, call.name, len(call.arguments)))

  # binop is of type BinaryOperation
  def compile_binaryop(self, jclass, sb, binop):
    self.compile_expression(jclass,sb, binop.left)

    self.compile_expression(jclass, sb, binop.right)

    if binop.operator in binopmap:
      self.out.write("%s\n" % binopmap[binop.operator])

  # unop is of type UnaryOperation
  def compile_unaryop(self, jclass, sb, unop):
    self.compile_expression(jclass,sb,unop.argument)

    if (unop.operator == '-'):
      self.out.write("neg\n")
    elif unop.operator == '~':
      self.out.write("not\n")


# --------------------------------------------------------------------

def main():
  if len(sys.argv) != 2:
    sys.stderr.write("Usage: python3 jackcompiler.py <file.jack>\n")
    sys.stderr.write("    or python3 jackcompiler.py <directory>\n")    
    sys.exit(9)
  path = sys.argv[-1]
  fnames = []
  if path.endswith(".jack"):
    i = path.rfind("/")
    folder = path[:i]
    fnames.append(path)
  else:
    folder = path
    for fname in os.listdir(path):
      if fname.endswith(".jack"):
        fnames.append(path + "/" + fname)
  jclasses = []
  try:
    for fname in fnames:
      jclasses.append(jackparser.parse(fname))
  except jackparser.InputError as e:
    print("Error:", e.msg)
    print("In file '%s', line %d, column %d" %
          (e.token.fname, e.token.lineno, e.token.pos))
    return
  # parsing succeeded, now compile to VM
  tokenizer = tokens.Tokenizer(folder + '/Main.jack')
  compiler = JackCompiler(folder, tokenizer)
  for jclass in jclasses:
    compiler.compile(jclass)

# --------------------------------------------------------------------

if __name__ == "__main__":
  main()

# --------------------------------------------------------------------
