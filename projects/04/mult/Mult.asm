// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[3], respectively.)

// Start with R2 as 0
@R2
M=0

// While R1>1, add the value in R0 to D
(LOOP)
    // if R1<=0, break
    @R1
    D=M
    @END
    D;JLE

    // add contents of R0 to R2
    @R0
    D=M
    @R2
    M=D+M
    
    // decrement R1
    @R1
    M=M-1

    // Return to top of loop
    @LOOP
    0;JMP


// ending loop
(END)
@END
0;JMP
