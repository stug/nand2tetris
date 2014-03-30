// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// initialize R0 to 0 (we'll store which we're painting 0's or 1's here)
@R0
M=0

(STARTLOOP)
    // check keyboard and jump appropriately
    @KBD
    D=M
    @SETBLACK
    D;JNE

    // set R0 to 0 so we paint the screen white. We'll only get here if we
    // didn't jump
    @R0
    M=0
    @PAINTSCREEN
    0;JMP

    // set R0 to -1 (all 1's in 2's complement) so we paint the screen black.
    // No need to jump to PAINTSCREEN since it comes next anyway
    (SETBLACK)
    @R0
    M=-1

    (PAINTSCREEN)
    // store current position on screen in R1
    @SCREEN
    D=A
    @R1
    M=D
    
    (STARTPAINT)
        // start over if we've painted the whole screen (KBD comes after screen,
        // so using that to tell if we're past the screen...kind of a hack)
        @KBD
        D=A
        @R1
        D=D-M
        @STARTLOOP
        D;JEQ

        // store value to paint in D
        @R0
        D=M

        // jump to position we're painting
        @R1
        A=M

        M=D  // paint!

        // increment R1 and return to top
        @R1
        M=M+1
        @STARTPAINT
        0;JMP


