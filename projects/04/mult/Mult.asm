// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// add R1, R2 times

//int i = R1;
//int sum = 0;
//while (i != 0) {
//  sum += R0;
//  i--;
//}

//int i = R0;
//int j = R1;
//if (i < j) :
  // add j , i times.
  // if i > 128 :
  
//else :
 // add i , j times

  @sum
  M = 0
  @R0
  D = M
  @i
  M = D // i = R1
  @R1
  D = M
  @j
  M = D // j = R2
  D = M
  @i 
  D = D - M // D = j - i
  @J_LESS_THAN_I
  D ; JLT
  @I_LESS_THAN_J
  0; JMP
(J_LESS_THAN_I) // R1 < R0 -> multiply R0(i) R1(j) times
  @128
  D = A
  @j
  D = M-D // j - 128
  @BIGNUM_J
  D; JGE
  @j
  D = M
  @END
  D;JEQ
  @R0
  D = M
  @sum
  M = D+M
  @j
  M = M -1
  @J_LESS_THAN_I
  0;JMP
(I_LESS_THAN_J)
  @i
  D = M
  @END
  D;JEQ
  @R1
  D = M
  @sum
  M = D+M
  @i 
  M = M-1
  @I_LESS_THAN_J
  0;JMP
(BIGNUM_J)
  @128
  D = A
  @k
  M = D
  @j
  D = M
  @k
  M = D - M // k = j - 100 for checking
  @counter 
  M = 1
  @R0
  D = M
  @sum
  M = D
(MINILOOP)
  @128
  D = A
  @counter
  D = D - M // D = 100 - counter
  @REMAINDER
  D; JEQ
  @sum 
  D = M
  M = M + D
  @counter
  D = M
  M = M + D
  @MINILOOP
  0;JMP
(REMAINDER)
  @k
  D = M
  @END
  D; JEQ
  @R0
  D = M
  @sum
  M = M + D
  @k
  M = M -1
  @REMAINDER
  0;JMP
(END)
  @sum
  D = M
  @R2
  M = D
  @END
  0;JMP
  



