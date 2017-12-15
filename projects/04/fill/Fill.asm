// Put your code here.

  @SCREEN
  D = A
  @i
  M = 0
  @i
  M = D // i = 16384

// if keyboard==true, color, else clear 
(LOOP)
  @KBD
  D=M
  @COLOR
  D;JGT
  @CLEAR
  0;JMP

(COLOR)
  @i
  D = M
  // if i > 24575 : go to loop
  @24575
  D = D - A
  @LOOP
  D;JGT
  //else color
  @i
  A=M
  M=-1
  @i
  M=M+1
  @LOOP
  0;JMP

(CLEAR)
  // if i < 16384 : loop
  @i
  D=M
  @SCREEN
  D=D-A
  @LOOP
  D;JLT
  // else clear
  @i
  A=M
  M=0
  @i
  M=M-1
  @LOOP
  0;JMP

  






