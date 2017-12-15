import sys

next_mem_addr = 15
curr_addr = 0

comp_field = {
        '0' : "101010",
        '1' : "111111",
        '-1' : "111010",
        'D' : "001100",
        'A' : "110000",
        'M' : "110000",
        '!D' : "001101",
        '!A' : "110001",
        '!M' : "110001",
        '-D' : "001111",
        '-A' : "110011",
        '-M' : "110011",
        'D+1' : "011111",
        'A+1' : "110111",
        'M+1' : "110111",
        'D-1' : "001110",
        'A-1' : "110010",
        'M-1' : "110010",
        'D+A' : "000010",
        'D+M' : "000010",
        'D-A' : "010011",
        'D-M' : "010011",
        'A-D' : "000111",
        'M-D' : "000111",
        'D&A' : "000000",
        'D&M' : "000000",
        'D|A' : "010101",
        'D|M' : "010101"
        }

dest = {
        'M' : "001",
        'D' : "010",
        'MD' : "011",
        'A' : "100",
        'AM' : "101",
        'AD' : "110",
        'AMD' : "111"
        }

jump = {
        'JGT' : "001",
        'JEQ' : "010",
        'JGE' : "011",
        'JLT' : "100",
        'JNE' : "101",
        'JLE' : "110",
        'JMP' : "111"
        }

class SymbolTable (object) :
    def __init__(self):
        self.entry = {
                'SP' : 0,
                'LCL' : 1,
                'ARG' : 2,
                'THIS' : 3,
                'THAT' : 4,
                'R0' : 0,
                'R1' : 1,
                'R2' : 2,
                'R3' : 3,
                'R4' : 4,
                'R5' : 5,
                'R6' : 6,
                'R7' : 7,
                'R8' : 8,
                'R9' : 9,
                'R10' : 10,
                'R11' : 11,
                'R12' : 12,
                'R13' : 13,
                'R14' : 14,
                'R15' : 15,
                'SCREEN' : 16384,
                'KBD' : 24576
                }

    def addEntry(self, symbol, memaddr):
        self.entry[symbol] = memaddr

    def contains(self, symbol):
        check = symbol in self.entry
        return check

    def getAddress(self, symbol):
        addr = self.entry[symbol]
        return addr

def readFileName():
    filename = sys.argv[-1]
    return filename

def hasMoreCommands():
    pass

def advance():
    pass

def commandType(command):
    if (command[0] == '/') :
        return
    command = command.strip('   ')
    if (command[0] == '('):
        return "FUNC" 
    elif (command[0] == '@'):
        return "A_COMMAND"
    else :
        cmd_parse = command.split(';')
        if (cmd_parse[0] == '\n'):
            return
        elif len(cmd_parse) == 1:
            return "L_COMMAND"
        elif len(cmd_parse) > 1:
            return "C_COMMAND"
        else :
            return 

def parseLine(line, writefile, second_pass,symtable):
    global curr_addr
    global next_mem_addr

    # get command type
    cmd_type = commandType(line)

    # if it is just a comment or empty line, skip
    if (cmd_type == None):
        return

    # remove all unnecessary characters
    line = line.strip(' ').strip('\n')

    # first pass : add all function positions
    if not second_pass:
        if cmd_type == "FUNC":
            symtable.addEntry(line[1:-1], curr_addr)
        else :
            curr_addr +=1

    # second pass
    else : 
        if (cmd_type == "A_COMMAND"):
            val = line.strip('\n').strip('@').strip('  ')
            if not val.isdigit():
                # if it is a new variable
                if not symtable.contains(val):
                    next_mem_addr +=1
                    symtable.addEntry(val, next_mem_addr)
                    binval = next_mem_addr
                else : 
                    binval= symtable.getAddress(val)
            else :
                binval = val
            # convert to binary
            binval = ''.join(format(int(binval), 'b'))
            binval = binval.zfill(16)
            writefile.write(binval + '\n')
        elif (cmd_type == "L_COMMAND"):
            parsed_line = line.split('=')
            d = dest[parsed_line[0]]
            parsed_line = parsed_line[1].split('//')
            tmp = parsed_line[0].split(' ')
            c = comp_field[tmp[0]]
            # check for memory access
            for char in str(tmp) :
                if (char == 'M'):
                    a = '1'
                    break
                else :
                    a = '0'
            wrt = '111' + a + c + d + '000\n'
            writefile.write(wrt)

        elif (cmd_type == "C_COMMAND"):
            # need 2 splits. first one with ';' and second with '='
            parsed_line = line.split(';')
            second_parsed_line = parsed_line[1].split('//')[0].split(' ')[0]
            j = jump[second_parsed_line]
            parsed_comp = parsed_line[0].split('=')
            # if no '=' then dest is omitted 
            if  len(parsed_comp) == 1: 
                d = '000'
            else :
                d = dest[parsed_comp[0]]

            if len(parsed_comp) == 1 :
                check = parsed_comp[0]
                c = comp_field[check]
            else : 
                check = parsed_comp[1]
                c = comp_field[check]
        
            # check for memory access
            for char in str(check) :
                if (char == 'M'):
                    a = '1'
                    break
                else :
                    a = '0'
            wrt = '111' + a + c + d + j + '\n'
            writefile.write(wrt)


if __name__ == "__main__":
    filename = readFileName()
    f = open(filename, 'r')
    filepath = filename.rsplit('/',1)[0]
    parsed_filename = filename.split('/')[-1].split('.')[0]
    writefile = open(filepath + '/' + parsed_filename + '.hack', 'w')

    symtable = SymbolTable()
    # first pass
    for line in f:
        parseLine(line,writefile,0, symtable)

    f.close()
    f = open(filename, 'r')
    # second pass
    for line in f:
        parseLine(line, writefile, 1,symtable)

    f.close()
    writefile.close()
    

