from contextlib import contextmanager

from arithmetic_command_builder import ArithmeticCommandBuilder
from push_pop_command_builder import PushPopCommandBuilder
from commands import ComparisonCommand
from commands import OneOperandArithmeticCommand
from commands import PushPopCommand
from commands import TwoOperandArithmeticCommand


class CodeWriter(object):
    """Reserved registers:
    - R13 register is used to return to previous execution context after a jump
    """

    def __init__(self, output_filename):
        self.output_filename = output_filename
        self.output_file = None
        self.arithmetic_command_builder = ArithmeticCommandBuilder()
        self.push_pop_command_builder = PushPopCommandBuilder()

        self.vm_command_type_to_method = {
            ComparisonCommand: self.arithmetic_command_builder.build_comparison,
            OneOperandArithmeticCommand: self.arithmetic_command_builder.build_one_operand_arithmetic,
            TwoOperandArithmeticCommand: self.arithmetic_command_builder.build_two_operand_arithmetic,
            PushPopCommand: self.push_pop_command_builder.build_push_pop
        }

    @contextmanager
    def open(self):
        with open(self.output_filename, 'w') as self.output_file:
            self.write_initialization()
            yield self

    def write_initialization(self):
        # TODO: should each setup piece have its own method?
        asm_commands = [
            # initialize stack pointer to 256 and then jump to after definition
            # of SETTRUE
            '@256',
            'D=A',
            '@SP',
            'M=D',
            '@STARTPROGRAM',
            'D;JMP',
            '',
            # replace top of stack with true and jump back to instruction
            # stored in R13
            '(SETTRUE)',
            '@SP',
            'A=M-1',  # decrement because the top of the stack is 1 before @SP
            'M=-1',
            '@R13',
            'A=M',
            'D;JMP',
            '',
            '(STARTPROGRAM)'
        ]
        self.write_asm_commands(asm_commands)

    def set_vm_filename(self, vm_filename):
        self.push_pop_command_builder.set_current_vm_filename(vm_filename)

    def write_asm_commands(self, asm_commands):
        self.output_file.write('\n'.join(asm_commands))
        self.output_file.write('\n\n')

    def translate_and_write_vm_command(self, command):
        asm = ['//{}'.format(str(command))]
        asm += self.vm_command_type_to_method[type(command)](command)
        self.write_asm_commands(asm)

