// Initialize stack pointer
@256
D=A
@SP
M=D

//call Sys.init 0
// Save return address to stack
@$$call$$0
D=A
@SP
A=M
M=D
@SP
M=M+1

// Save LCL to stack
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save ARG to stack
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THIS to stack
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THAT to stack
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// set ARG pointer
@SP
D=M
@5
D=D-A
@ARG
M=D

// set LCL=SP
@SP
D=M
@LCL
M=D

// jump to function label
@Sys.init
D;JMP
($$call$$0)

// SETTRUE label sets top of stack to True and jumps back to 
// instruction address stored in R13
(SETTRUE)
@SP
A=M-1
M=-1
@R13
A=M
D;JMP

//function Main.fibonacci 0
(Main.fibonacci)

//push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt 
@lt.0
D=A
@R13
M=D
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=D-M
M=0
@SETTRUE
D;JGT
(lt.0)

//if-goto IF_TRUE
@SP
M=M-1
A=M
D=M
@Main.fibonacci$IF_TRUE
D;JNE

//goto IF_FALSE
@Main.fibonacci$IF_FALSE
D;JMP

//label IF_TRUE
(Main.fibonacci$IF_TRUE)

//push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//return 
// store return address in R13
@5
D=A
@LCL
A=M-D
D=M
@R13
M=D

// put return value where ARG currently points (will be top of stack)
@SP
A=M-1
D=M
@ARG
A=M
M=D

// move SP to one after return value we just placed
D=A+1
@SP
M=D

// restore THAT
@LCL
D=M
@1
A=D-A
D=M
@THAT
M=D

// restore THIS
@LCL
D=M
@2
A=D-A
D=M
@THIS
M=D

// restore ARG
@LCL
D=M
@3
A=D-A
D=M
@ARG
M=D

// restore LCL
@LCL
D=M
@4
A=D-A
D=M
@LCL
M=D

// jump to stored return address
@R13
A=M
0;JMP


//label IF_FALSE
(Main.fibonacci$IF_FALSE)

//push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=-D
M=D+M

//call Main.fibonacci 1
// Save return address to stack
@Main.fibonacci$$call$$1
D=A
@SP
A=M
M=D
@SP
M=M+1

// Save LCL to stack
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save ARG to stack
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THIS to stack
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THAT to stack
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// set ARG pointer
@SP
D=M
@6
D=D-A
@ARG
M=D

// set LCL=SP
@SP
D=M
@LCL
M=D

// jump to function label
@Main.fibonacci
D;JMP
(Main.fibonacci$$call$$1)

//push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=-D
M=D+M

//call Main.fibonacci 1
// Save return address to stack
@Main.fibonacci$$call$$2
D=A
@SP
A=M
M=D
@SP
M=M+1

// Save LCL to stack
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save ARG to stack
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THIS to stack
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THAT to stack
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// set ARG pointer
@SP
D=M
@6
D=D-A
@ARG
M=D

// set LCL=SP
@SP
D=M
@LCL
M=D

// jump to function label
@Main.fibonacci
D;JMP
(Main.fibonacci$$call$$2)

//add 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M

//return 
// store return address in R13
@5
D=A
@LCL
A=M-D
D=M
@R13
M=D

// put return value where ARG currently points (will be top of stack)
@SP
A=M-1
D=M
@ARG
A=M
M=D

// move SP to one after return value we just placed
D=A+1
@SP
M=D

// restore THAT
@LCL
D=M
@1
A=D-A
D=M
@THAT
M=D

// restore THIS
@LCL
D=M
@2
A=D-A
D=M
@THIS
M=D

// restore ARG
@LCL
D=M
@3
A=D-A
D=M
@ARG
M=D

// restore LCL
@LCL
D=M
@4
A=D-A
D=M
@LCL
M=D

// jump to stored return address
@R13
A=M
0;JMP


//function Sys.init 0
(Sys.init)

//push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Main.fibonacci 1
// Save return address to stack
@Sys.init$$call$$3
D=A
@SP
A=M
M=D
@SP
M=M+1

// Save LCL to stack
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save ARG to stack
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THIS to stack
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

// Save THAT to stack
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

// set ARG pointer
@SP
D=M
@6
D=D-A
@ARG
M=D

// set LCL=SP
@SP
D=M
@LCL
M=D

// jump to function label
@Main.fibonacci
D;JMP
(Sys.init$$call$$3)

//label WHILE
(Sys.init$WHILE)

//goto WHILE
@Sys.init$WHILE
D;JMP

