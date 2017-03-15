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

//push constant 10
@10
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop local 0
@0
D=A
@LCL
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

//push constant 21
@21
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 22
@22
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop argument 2
@2
D=A
@ARG
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

//pop argument 1
@1
D=A
@ARG
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

//push constant 36
@36
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop this 6
@6
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

//push constant 42
@42
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 45
@45
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop that 5
@5
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

//pop that 2
@2
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

//push constant 510
@510
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop temp 6
@6
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

//push local 0
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//push that 5
@5
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

//sub 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=-D
M=D+M

//push this 6
@6
D=A
@THIS
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1

//push this 6
@6
D=A
@THIS
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

//sub 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
D=-D
M=D+M

//push temp 6
@6
D=A
@R5
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

