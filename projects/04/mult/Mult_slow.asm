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


// load R2
  @sum
  M = 0
  @R2
  M = 0
  @R1
  D = M
  @i
  M = D

(LOOP)
  @i
  D = M
  @END
  D;JEQ
  @R0
  D = M
  @sum
  M = D + M
  D = M
  @R2
  M = D
  @i
  M = M - 1
  @LOOP
  0;JMP
  // D;jeq
(END)
  @END
  0;JMP
  



