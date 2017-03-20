@256
D=A
@SP
M=D
@STARTPROGRAM
D;JMP

(SETTRUE)
@SP
A=M-1
M=-1
@R13
A=M
D;JMP

(STARTPROGRAM)

//push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop static 8
@StaticTest.vm.8
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

//pop static 3
@StaticTest.vm.3
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

//pop static 1
@StaticTest.vm.1
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

//push static 3
@StaticTest.vm.3
D=M
@SP
A=M
M=D
@SP
M=M+1

//push static 1
@StaticTest.vm.1
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

//push static 8
@StaticTest.vm.8
D=M
@SP
A=M
M=D
@SP
M=M+1

//add 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M

