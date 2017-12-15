@sum   // address of the currently coloring word
M=0
@SCREEN
D=A
@31
D=D+A
@sum
M=D  // sum = 16384 + 31
(LOOP)
// 1100,0000,0000,0000  start with right most 2 bits
@16383
D=A
D=-D
D=D-1
@sum
A=M
M=D  
@32
D=A
@sum
M=M+D // sum+32
// 0011,0000,0000,0000
@12288
D=A
@sum
A=M
M=D
@32
D=A
@sum
M=M+D // sum + 32
// 0000,1100,0000,0000
@3072
D=A
@sum
A=M
M=D
@32
D=A
@sum
M=M+D
// 0000,0011,0000,0000
@768
D=A
@sum
A=M
M=D
@32
D=A
@sum
M=M+D
// 0000,0000,1100,0000
@192
D=A
@sum
A=M
M=D
@32
D=A
@sum
M=M+D
// 0000,0000,0011,0000
@48
D=A
@sum
A=M
M=D
@32
D=A
@sum
M=M+D
// 0000,0000,0000,1100
@12
D=A
@sum
A=M
M=D
@32
D=A
@sum
M=M+D
// 0000,0000,0000,0011
@3
D=A
@sum
A=M
M=D
@31  // add 31 because it is one word(4bytes) left of current column
D=A
@sum
M=M+D
// check if out of range
@24575
D=A
@sum
D= M-D
@END
D;JGE
@LOOP
0;JMP
(END)
@END
0;JMP


