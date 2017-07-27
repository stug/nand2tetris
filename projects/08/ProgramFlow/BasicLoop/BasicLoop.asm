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

//push constant 0
@0
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

//label LOOP_START
($LOOP_START)

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

//add 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D+M

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

//pop argument 0
@0
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

//if-goto LOOP_START
@SP
M=M-1
A=M
D=M
@$LOOP_START
D;JNE

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

