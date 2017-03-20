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

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq 
@eq.0
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
D;JEQ
(eq.0)

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq 
@eq.1
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
D;JEQ
(eq.1)

//push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1

//eq 
@eq.2
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
D;JEQ
(eq.2)

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt 
@lt.3
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
(lt.3)

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt 
@lt.4
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
(lt.4)

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1

//lt 
@lt.5
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
(lt.5)

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt 
@gt.6
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
D;JLT
(gt.6)

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt 
@gt.7
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
D;JLT
(gt.7)

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1

//gt 
@gt.8
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
D;JLT
(gt.8)

//push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant 53
@53
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

//push constant 112
@112
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

//neg 
@SP
A=M-1
M=-M

//and 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D&M

//push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1

//or 
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=D|M

//not 
@SP
A=M-1
M=!M

