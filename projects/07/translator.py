import sys

# reads the file
class VMParser:
    def __init__(self, filename):
        self.filename = filename
        self.curr_instr = None
        self.next_instr = None
        self.file = None
        self.file = open(self.filename,'r')
        self.file_init()

    # find out what type of instruction it is
    def get_command_type(self):
        cmd_types=  {
                'push' : 'VM_PUSH',
                'pop'  : 'VM_POP',
                'add'  : 'VM_ARITH',
                'sub'  : 'VM_ARITH',
                'not'  : 'VM_NOT',
                'neg'  : 'VM_NEG',
                'eq'   : 'VM_COMP',
                'gt'   : 'VM_COMP',
                'lt'   : 'VM_COMP',
                'and'  : 'VM_ARITH',
                'or'   : 'VM_ARITH',
                'label': 'VM_LABEL',
                'goto' : 'VM_GOTO',
              'if-goto': 'VM_IF_GOTO',
            'function' : 'VM_FUNCTION',
              'return' : 'VM_RETURN',
                'call' : 'VM_CALL'
                }
        cmd = cmd_types[self.curr_instr.split()[0]]
        print (cmd)
        return cmd

    def file_init(self):
        line = self.file.readline().strip()
        while line[:2] == '//':
            line = self.file.readline().strip()
        self.curr_instr = line
        self.next_instr = self.get_next_instr()
   
    # read next line 
    def get_next_instr(self):
        line = self.file.readline().strip()
        while line[:2] == '//':
            line = self.file.readline().strip()
        return line

    # update current and next instruction 
    def next(self):
        self.curr_instr = self.next_instr
        self.next_instr = self.get_next_instr()
        print ('next\n')
        print ('curr instr : ' + self.curr_instr)
        print ('next instr : ' + self.next_instr)

    # is end of file. no more instruction
    def is_end(self):
        if self.next_instr == '':
            return True
        return False



# writes to file
class HackGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'w')
        self.cond_jump_count = 0
        self.call_count = 0

    # put value of D into stack
    def stack_push (self):
        self.file.write('@SP\n')
        self.file.write('A=M\n')
        self.file.write('M=D\n')
        self.file.write('@SP\n')
        self.file.write('M=M+1\n')

    # get value of stack into D
    def stack_pop (self):
        self.file.write('@SP\n')
        self.file.write('AM=M-1\n')
        self.file.write('D=M\n')
    
    # push and pop instr
    def convert_stack_instr(self, op, var_type, var):
        # check the symbol register table 
        # if not in the symbol table, just write the value
        self.get_symbol_register(op, var_type, var)
        if op == 'VM_PUSH':
            self.stack_push()

        elif op == 'VM_POP':
            self.file.write('@R13\n') # general purpose register
            self.file.write('M=D\n')
            self.stack_pop()
            self.file.write('@R13\n')
            self.file.write('A=M\n')
            self.file.write('M=D\n')

    # add, sub, and, or etc
    def convert_arithmetic_op(self, op):
        if not op in ['neg', 'not']:
            self.stack_pop() # D = value at stack
        self.file.write('@SP\n')
        self.file.write('M=M-1\n') # decrease SP
        self.file.write('@SP\n')
        self.file.write('A=M\n')
        # A = stack address, save value into stack
        if op == 'add':
            self.file.write('M=M+D\n')
        elif op == 'sub':
            self.file.write('M=M-D\n')
        elif op == 'and':
            self.file.write('M=M&D\n')
        elif op == 'or':
            self.file.write('M=M|D\n')
        elif op == 'neg':
            self.file.write('M=-M\n')
        elif op == 'not':
            self.file.write('M=!M\n')
        
        self.file.write('@SP\n')
        self.file.write('M=M+1\n')
    
    # eq, lt, gt etc
    def convert_comparison(self, op):
        self.stack_pop() # D = value at stack
        self.file.write('@SP\n')
        self.file.write('M=M-1\n') # decrease SP
        self.file.write('@SP\n')
        self.file.write('A=M\n')
        
        self.file.write('D=M-D\n')
        self.file.write('@COND_JUMP%d\n' %self.cond_jump_count)
        if op == 'eq':
            self.file.write('D;JEQ\n')
        if op == 'lt':
            self.file.write('D;JLT\n')
        if op == 'gt':
            self.file.write('D;JGT\n')
        
        self.file.write('@SP\n')
        self.file.write('A=M\n')
        self.file.write('M=0\n')
        self.file.write('@EXIT%d\n' % self.cond_jump_count)
        self.file.write('0;JMP\n')

        self.file.write('(COND_JUMP%d)\n' %self.cond_jump_count)
        self.file.write('@SP\n')
        self.file.write('A=M\n')
        self.file.write('M=-1\n') # set to true
        
        self.file.write('(EXIT%d)\n' %self.cond_jump_count)

        self.file.write('@SP\n')
        self.file.write('M=M+1\n')
        self.cond_jump_count += 1

    def convert_label (self, label) :
        self.file.write('(' + label + ')\n')
        
    def convert_goto(self, label):
        self.file.write('@' + label + '\n')
        self.file.write('0;JMP\n')

    def convert_ifgoto(self, label):
        self.stack_pop()
        self.file.write('@' + label + '\n')
        self.file.write('D;JNE\n')

    def convert_return(self):
        # clear function's argument
        self.file.write('@LCL\n')
        self.file.write('D=M\n')
        self.file.write('@R13\n') # FRAME
        self.file.write('M=D\n') 
        
        self.file.write('@R13\n')
        self.file.write('D=M\n')
        self.file.write('@5\n')
        self.file.write('AD=D-A\n')
        self.file.write('D=M\n')
        self.file.write('@R14\n') # RET
        self.file.write('M=D\n')
       
        self.stack_pop()  
        self.file.write('@ARG\n')
        self.file.write('A=M\n')
        self.file.write('M=D\n')

        # SP = ARG + 1
        self.file.write('@ARG\n')
        self.file.write('D=M\n')
        self.file.write('@SP\n')
        self.file.write('M=D+1\n')

        # restore parent vars
        for var in ['THAT', 'THIS', 'ARG', 'LCL']:
            self.file.write('@R13\n')
            self.file.write('AM=M-1\n')
            self.file.write('D=M\n')
            self.file.write('@' + var + '\n')
            self.file.write('M=D\n')

        # jump to saved return address
        self.file.write('@R14\n')
        self.file.write('A=M\n')
        self.file.write('0;JMP\n')


    # push as many args as needed : arg2 = g, arg3 = nVars 
    def convert_function (self, arg2, arg3):
        self.file.write('(' + arg2 + ')\n')
        for i in range(int(arg3)):
            self.file.write('D=0\n')
            self.stack_push()

    def convert_call (self, arg2, arg3):
        # save return address
        self.file.write('@RETURN%d\n' % self.call_count) 
        self.file.write('D=A\n')
        self.stack_push()
        
        # push parent vars
        for var in ['LCL', 'ARG', 'THIS', 'THAT', ]:
            self.file.write('@' + var + '\n')
            self.file.write('D=M\n')
            self.stack_push()
        
        self.file.write('@SP\n')
        self.file.write('D=M\n')
        self.file.write('@' + str(int(arg3) + 5)+ '\n')
        self.file.write('D=D-A\n') # SP - nvars - 5
        self.file.write('@ARG\n')
        self.file.write('M=D\n')
        
        # LCL = SP
        self.file.write('@SP\n')
        self.file.write('D=M\n')
        self.file.write('@LCL\n')
        self.file.write('M=D\n')
        
        # go to g 
        self.file.write('@' + arg2 + '\n')
        self.file.write('0;JMP\n')
        
        # place the return function here
        self.file.write('(RETURN%d)\n'%self.call_count)
        self.call_count += 1

    # for push and pop instructions, need to find the correct symbol
    # save the caculated address in D
    def get_symbol_register(self, arg1, var_type, var ):
        symbol_regs = {
                    'local': 'LCL',
                    'this' : 'THIS',
                    'that' : 'THAT',
                    'argument' : 'ARG',
                }
        if var_type in ['local', 'this' ,'that', 'argument']:
            self.file.write('@' + symbol_regs[var_type] + '\n')
            self.file.write('D=M\n')
            self.file.write('@' + var+'\n')
            self.file.write('A=D+A\n')
            if arg1 == 'VM_POP':
                self.file.write('D=A\n')
            elif arg1 =='VM_PUSH':
                self.file.write('D=M\n')
        elif var_type == 'temp':
            self.file.write('@R' + str(int(var) + 5) + '\n')
            if arg1 == 'VM_POP':
                self.file.write('D=A\n')
            elif arg1 == 'VM_PUSH':
                self.file.write('D=M\n')
        elif var_type == 'pointer':
            self.file.write('@R' + str(int(var) + 3) + '\n')
            if arg1 == 'VM_PUSH':
                self.file.write('D=M\n')
            elif arg1 == 'VM_POP':
                self.file.write('D=A\n')
        elif var_type == 'static':
            self.file.write('@R' + str(int(var) + 16) + '\n')
            if arg1 == 'VM_POP':
                self.file.write('D=A\n')
            elif arg1 == 'VM_PUSH':
                self.file.write('D=M\n')
        elif var_type == 'constant':
            self.file.write('@' + str(var) + '\n')
            self.file.write('D=A\n')

if __name__ == '__main__':
    filename = sys.argv[-1]
    print (filename)
    vmparser = VMParser(filename)
    asmfilename = filename.split('.')[0]
    hackgenerator = HackGenerator(asmfilename + '.asm')
    while not vmparser.is_end():
        vmparser.next()
        cmd = vmparser.get_command_type()
        inst = vmparser.curr_instr.split()
        if cmd == 'VM_PUSH' or cmd == 'VM_POP':
            hackgenerator.convert_stack_instr(cmd, inst[1], inst[2])
        elif cmd in  ['VM_ARITH', 'VM_NEG', 'VM_NOT']:
            hackgenerator.convert_arithmetic_op(inst[0])
        elif cmd == 'VM_COMP':
            hackgenerator.convert_comparison(inst[0])
        elif cmd == 'VM_LABEL':
            hackgenerator.convert_label (inst[1])
        elif cmd == 'VM_GOTO' :
            hackgenerator.convert_goto(inst[1])
        elif cmd == 'VM_IF_GOTO' :
            hackgenerator.convert_ifgoto(inst[1])
        elif cmd == 'VM_FUNCTION':
            hackgenerator.convert_function(inst[1], inst[2])
        elif cmd == 'VM_RETURN' :
            hackgenerator.convert_return()
        elif cmd == 'VM_CALL':
            hackgenerator.convert_call(inst[1], inst[2])
        #print ('loop: ' + vmparser.curr_instr)



