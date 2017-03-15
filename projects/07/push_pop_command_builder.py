from collections import namedtuple


class PushPopCommandBuilder(object):

    # assumes the value we want to push is in the D register
    PUSH_COMMAND_BASE = [
        # Store D in top of stack
        '@SP',
        'A=M',
        'M=D',

        # increment stack pointer
        '@SP',
        'M=M+1'
    ]

    # assumes we are starting with the index that we are popping to in the
    # A register
    POP_COMMAND_BASE = [
        # store location popped value will go to in R14
        'D=A',
        '@R14',
        'M=D',

        # Store top of stack in D
        '@SP',
        'A=M-1',
        'D=M',

        # decrement stack pointer
        '@SP',
        'M=M-1',

        # store the value from the stack in the location previously stored in
        # R14
        '@R14',
        'A=M',
        'M=D'
    ]

    MEMORY_SEGMENT_TO_BASE_ADDRESS = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'pointer': 'R3',
        'temp': 'R5'
    }

    def __init__(self):
        self.current_vm_filename = None

        # commands that leave the A register pointing to the memory location
        # specified by the command's memory segment and index
        self.segment_to_access_commands_builder = {
            'local': self.build_dynamic_memory_segment_access_commands,
            'argument': self.build_dynamic_memory_segment_access_commands,
            'this':self.build_dynamic_memory_segment_access_commands,
            'that': self.build_dynamic_memory_segment_access_commands,

            'temp': self.build_fixed_memory_segment_access_commands,
            'pointer': self.build_fixed_memory_segment_access_commands,

            'constant': self.build_constant_memory_segment_access_commands,
            'static': self.build_static_memory_segment_access_commands
        }

    def set_current_vm_filename(self, vm_filename):
        self.current_vm_filename = vm_filename

    def build_push_pop(self, command):
        asm_commands = self.segment_to_access_commands_builder[command.memory_segment](command)
        if command.command_name == 'push':
            return asm_commands + self.build_push_commands(command)
        else:
            return asm_commands + self.build_pop_commands(command)

    def build_push_commands(self, command):
        if command.memory_segment == 'constant':
            asm_commands = ['D=A']
        else:
            asm_commands = ['D=M']

        return asm_commands + self.PUSH_COMMAND_BASE

    def build_pop_commands(self, command):
        return self.POP_COMMAND_BASE

    def build_constant_memory_segment_access_commands(self, command):
        return [
            '@{}'.format(command.index)
        ]

    def build_dynamic_memory_segment_access_commands(self, command):
        return [
            '@{}'.format(command.index),
            'D=A',
            '@{}'.format(self.MEMORY_SEGMENT_TO_BASE_ADDRESS[command.memory_segment]),
            'A=D+M',
        ]

    def build_fixed_memory_segment_access_commands(self, command):
        return [
            '@{}'.format(command.index),
            'D=A',
            '@{}'.format(self.MEMORY_SEGMENT_TO_BASE_ADDRESS[command.memory_segment]),
            'A=D+A',
        ]

    def build_static_memory_segment_access_commands(self, command):
        return [
            '@{vm_filename}.{index}'.format(
                vm_filename=self.current_vm_filename,
                index=command.index
            )
        ]
