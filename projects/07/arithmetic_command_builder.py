# TODO: this could probably be split up more
class ArithmeticCommandBuilder(object):

    def __init__(self):
        # for uniqueness of labels
        self.arbitrary_number = 0

    def get_arbitrary_number(self):
        arbitrary_number = self.arbitrary_number
        self.arbitrary_number += 1
        return arbitrary_number

    def build_end_label_name(self, command_name):
        return '{command_name}.{arbitrary_number}'.format(
            command_name=command_name,
            arbitrary_number=self.get_arbitrary_number()
        )

    ONE_OPERAND_ARITHMETIC_COMMAND_TO_ASM_COMP = {
        'neg': '-M',
        'not': '!M'
    }

    def build_one_operand_arithmetic(self, command):
        asm_commands = [
            '@SP',
            'A=M-1',  # because the number we are operating on is 1 before @SP
            'M={}'.format(
                self.ONE_OPERAND_ARITHMETIC_COMMAND_TO_ASM_COMP[command.command_name]
            )
        ]
        return asm_commands

    TWO_OPERAND_SETUP_COMMANDS = [
        # pop top element off stack and store in D register
        '@SP',
        'M=M-1',
        'A=M',
        'D=M',

        # store result of calculation in new top of stack
        '@SP',
        'A=M-1',  # top of stack is 1 before @SP
    ]

    TWO_OPERAND_ARITHMETIC_COMMAND_TO_ASM_COMP = {
        'add': ['M=D+M'],
        'sub': [
            'D=-D',
            'M=D+M'
        ],
        'and': ['M=D&M'],
        'or': ['M=D|M'],
    }

    def build_two_operand_arithmetic(self, command):
        asm_commands = list(self.TWO_OPERAND_SETUP_COMMANDS)  # new copy of setup
        asm_commands += self.TWO_OPERAND_ARITHMETIC_COMMAND_TO_ASM_COMP[command.command_name]
        return asm_commands

    COMPARISON_COMMAND_BASE = [
        'D=D-M',
        'M=0',
        '@SETTRUE',
    ]

    COMPARISON_COMMAND_TO_JUMP_TYPE = {
        'eq': 'JEQ',
        'gt': 'JLT',
        'lt': 'JGT'
    }

    def build_comparison(self, command):
        end_label = self.build_end_label_name(command.command_name)
        asm_commands = [
            '@{}'.format(end_label),
            'D=A',
            '@R13',
            'M=D'
        ]
        asm_commands += self.TWO_OPERAND_SETUP_COMMANDS
        asm_commands += self.build_comparison_base(command)
        asm_commands += ['({})'.format(end_label)]
        return asm_commands

    def build_comparison_base(self, command):
        comparison_jump_command = 'D;{jump_type}'.format(
            jump_type=self.COMPARISON_COMMAND_TO_JUMP_TYPE[command.command_name]
        )
        return self.COMPARISON_COMMAND_BASE + [comparison_jump_command]
