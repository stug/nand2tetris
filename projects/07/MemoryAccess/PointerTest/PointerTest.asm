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

//push constant 3030
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0
@0
D=A
@R3
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

//push constant 3040
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 1
@1
D=A
@R3
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

//push constant 32
@32
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop this 2
@2
D=A
@THIS
A=D+M
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

//push constant 46
@46
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop that 6
@6
D=A
@THAT
A=D+M
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

//push pointer 0
@0
D=A
@R3
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push pointer 1
@1
D=A
@R3
A=D+A
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

//push this 2
@2
D=A
@THIS
A=D+M
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

//push that 6
@6
D=A
@THAT
A=D+M
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

