import sys

# reads the file
class VMParser:
    def __init__(self, filename):
        self.filename = filename
        self.curr_instr = None
        self.next_instr = None
        self.file = None
        self.command_parser = self.command_parser()
        self.file = open(self.filename,'r')
        self.file_init()

    def command_parser(self):
        return {
                'push' : 'VM_PUSH',
                'pop'  : 'VM_POP',
                'add'  : 'VM_ADD',
                'sub'  : 'VM_SUB',
                'not'  : 'VM_NOT',
                'neg'  : 'VM_NEG',
                'eq'   : 'VM_EQ',
                'gt'   : 'VM_GT',
                'lt'   : 'VM_LT',
                'and'  : 'VM_AND',
                'or'   : 'VM_OR',
                'label': 'VM_LABEL',
                'goto' : 'VM_GOTO',
              'if-goto': 'VM_IF_GOTO',
            'function' : 'VM_FUNCTION',
              'return' : 'VM_RETURN',
                'call' : 'VM_CALL'
                }

    def file_init(self):
        line = self.file.readline().strip()
        while line[:2] == '//':
            line = self.file.readline().readline
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

    # is end of file. no more instruction
    def is_end(self):
        if self.next_instr == None:
            return True
        return False

    # find out what type of vm instruction it is 
    def get_command_type(self):
        cmd = self.command_parser[self.curr_instr[0]]
        print (cmd)
        return cmd



# writes to file
class HackGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'w')
    
    def set_SP(self, is_decrement):
        self.file.write('@SP\n')
        if is_decrement:
            self.file.write('M=M-1\n')
        else:
            self.file.write('M=M+1\n')

    # put value of D into stack
    def stack_push (self):
        self.file.write('@SP\n')
        self.file.write('A=M\n')
        self.file.write('M=D\n')
        self.file.write('@SP\n')
        self.file.write('M=M=1\n')

    # get value of stack into D
    def stack_pop (self):
        self.file.write('@SP\n')
        self.file.write('M=M-1\n')
        self.file.write('A=M\n')
        self.file.write('D=M\n')
    
    def convert_stack_instr(self, instr):
        # check the symbol register table 
        # if not in the symbol table, just write the value
        self.file.write('@\n')
        pass

    def convert_arithmetic_op(self, op):
        self.stack_pop() # D = value at stack
        self.file.write('@SP\n')
        self.file.write('M=M-1\n') # decrease SP
        
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
            self.file.write('M=~M\n')


    def get_symbol_register(self, var):
        symbol_regs = {
                    'local': 'LCL',
                    'this' : 'THIS',
                    'that' : 'THAT',
                    'static' : 16,
                    'pointer' : 3, 
                    'temp' : 5,
                    'argument' : 'ARG',
                }
        return symbol_regs[var]

if __name__ == '__main__':
    filename = sys.argv[-1]
    print (filename)
    '''
    try:
        fp = open(filename, 'r')
    except:
        print ("File not found")

    line = fp.readline()
    while line:
        if line[:2] == '//':
            pass
        else :
            print (line)
        line = fp.readline()
    '''

