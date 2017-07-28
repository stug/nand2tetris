from contextlib import contextmanager

from arithmetic_command_builder import ArithmeticCommandBuilder
from program_control_command_builder import ProgramControlCommandBuilder
from push_pop_command_builder import PushPopCommandBuilder
from commands import CallCommand
from commands import ComparisonCommand
from commands import FunctionCommand
from commands import ReturnCommand
from commands import OneOperandArithmeticCommand
from commands import ProgramFlowCommand
from commands import PushPopCommand
from commands import TwoOperandArithmeticCommand


class CodeWriter(object):

    def __init__(self, output_filename):
        self.output_filename = output_filename
        self.output_file = None
        self.arithmetic_command_builder = ArithmeticCommandBuilder()
        self.push_pop_command_builder = PushPopCommandBuilder()
        self.program_control_command_builder = ProgramControlCommandBuilder(
            self.push_pop_command_builder
        )

        # TODO: this is a little messy, maybe a metaclass is worth it after all?
        self.vm_command_type_to_method = {
            CallCommand: self.program_control_command_builder.build_call_command,
            ComparisonCommand: self.arithmetic_command_builder.build_comparison,
            FunctionCommand: self.program_control_command_builder.build_function_command,
            OneOperandArithmeticCommand: self.arithmetic_command_builder.build_one_operand_arithmetic,
            TwoOperandArithmeticCommand: self.arithmetic_command_builder.build_two_operand_arithmetic,
            PushPopCommand: self.push_pop_command_builder.build_push_pop,
            ProgramFlowCommand: self.program_control_command_builder.build_program_flow_command,
            ReturnCommand: self.program_control_command_builder.build_return_command,
        }

    @contextmanager
    def open(self):
        with open(self.output_filename, 'w') as self.output_file:
            self.write_initialization()
            yield self

    def write_initialization(self):
        self._write_initialize_stack_pointer()
        self.write_asm_commands(
            self.program_control_command_builder.build_call_sys_init()
        )
        self._write_create_set_true_label()

    def _write_initialize_stack_pointer(self):
        self.write_asm_commands([
            '// Initialize stack pointer',
            '@256',
            'D=A',
            '@SP',
            'M=D',
        ])

    def _write_create_set_true_label(self):
        self.write_asm_commands([
            '// SETTRUE label sets top of stack to True and jumps back to ',
            '// instruction address stored in R13',
            '(SETTRUE)',
            '@SP',
            'A=M-1',  # decrement because the top of the stack is 1 before @SP
            'M=-1',
            '@R13',
            'A=M',
            'D;JMP',
        ])

    def set_vm_filename(self, vm_filename):
        # TODO: might be nice to have some sort of proxy object instead of this
        self.push_pop_command_builder.set_current_vm_filename(vm_filename)
        self.program_control_command_builder.set_current_vm_filename(
            vm_filename
        )

    def write_asm_commands(self, asm_commands):
        self.output_file.write('\n'.join(asm_commands))
        self.output_file.write('\n\n')

    def translate_vm_command(self, command):
        asm = ['//{}'.format(str(command))]
        asm += self.vm_command_type_to_method[type(command)](command)
        return asm

    def translate_and_write_vm_command(self, command):
        asm = self.translate_vm_command(command)
        self.write_asm_commands(asm)

