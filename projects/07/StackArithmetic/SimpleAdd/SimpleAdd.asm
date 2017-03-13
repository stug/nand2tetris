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

//push constant 7
@7
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

//add 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M

