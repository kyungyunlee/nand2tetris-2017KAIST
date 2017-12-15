// compute R0/R1 = R2, R0%R1 = R3

// R2 = 0
// R3 = R0
// (LOOP)
// if R1 > R3 :
//    EXIT
// temp = R1     
// i = 1
// (LOOP2)
// if temp+temp > R3:
//    EXIT2
// temp = temp + temp
// i = i + i 
// goto LOOP2
//
// (EXIT2)
// R3 = R3 - temp
// R2 = R2 + i
// goto LOOP
//
// (EXIT)
// goto EXIT

@R2
M = 0
@R0
D = M
@R3
M = D
(LOOP)
@R3
D = M
@R1
D = M-D
@EXIT
D;JGT
@R1
D = M
@temp
M = D
@i
M = 1
(LOOP2)
@R3
D = M
@temp 
D = M - D
D = D + M
@EXIT2
D;JGT
@temp
D = M
M = M + D
@i
D = M
M = M + D
@LOOP2
0;JMP
(EXIT2)
@temp
D = M
@R3
M = M - D
@i
D = M
@R2
M = M + D
@LOOP
0;JMP
(EXIT)
@EXIT
0;JMP


