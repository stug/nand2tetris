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

//function Class1.set 0
(Class1.set)

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

//pop static 0
@Class1.vm.0
D=A
@R14
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@R14
A=M
M=D

//push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//pop static 1
@Class1.vm.1
D=A
@R14
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@R14
A=M
M=D

//push constant 0
@0
D=A
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


//function Class1.get 0
(Class1.get)

//push static 0
@Class1.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1

//push static 1
@Class1.vm.1
D=M
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

//push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Class1.set 2
// Save return address to stack
@Sys.init$$call$$1
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
@7
D=D-A
@ARG
M=D

// set LCL=SP
@SP
D=M
@LCL
M=D

// jump to function label
@Class1.set
D;JMP
(Sys.init$$call$$1)

//pop temp 0
@0
D=A
@R5
A=D+A
D=A
@R14
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@R14
A=M
M=D

//push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

//call Class2.set 2
// Save return address to stack
@Sys.init$$call$$2
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
@7
D=D-A
@ARG
M=D

// set LCL=SP
@SP
D=M
@LCL
M=D

// jump to function label
@Class2.set
D;JMP
(Sys.init$$call$$2)

//pop temp 0
@0
D=A
@R5
A=D+A
D=A
@R14
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@R14
A=M
M=D

//call Class1.get 0
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
@Class1.get
D;JMP
(Sys.init$$call$$3)

//call Class2.get 0
// Save return address to stack
@Sys.init$$call$$4
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
@Class2.get
D;JMP
(Sys.init$$call$$4)

//label WHILE
(Sys.init$WHILE)

//goto WHILE
@Sys.init$WHILE
D;JMP

//function Class2.set 0
(Class2.set)

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

//pop static 0
@Class2.vm.0
D=A
@R14
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@R14
A=M
M=D

//push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//pop static 1
@Class2.vm.1
D=A
@R14
M=D
@SP
A=M-1
D=M
@SP
M=M-1
@R14
A=M
M=D

//push constant 0
@0
D=A
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


//function Class2.get 0
(Class2.get)

//push static 0
@Class2.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1

//push static 1
@Class2.vm.1
D=M
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


