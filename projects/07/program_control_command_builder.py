from commands import ProgramFlowCommand
from commands import PushPopCommand


class ProgramControlCommandBuilder(object):

    def __init__(self, push_pop_command_builder):
        # having access to push pop commands simplifies function calling
        self.push_pop_command_builder = push_pop_command_builder

        self.current_vm_filename = None

        # current function definition we're in, used to ensure that labels
        # can be reused across functions without duplication in the resulting
        # assembly.
        self.current_function = None

        # arbitrary number used to unsure the uniqueness of labels used for
        # function return addresses
        self.arbitrary_number = 0

    def get_label_in_current_function_context(self, label):
        return '{function}${label}'.format(
            function=self.current_function or '',
            label=label,
        )

    def get_return_address_label(self):
        call_number = self.arbitrary_number
        self.arbitrary_number += 1
        return '{function}$$call$${number}'.format(
            function=self.current_function or '',
            number=call_number
        )

    def set_current_vm_filename(self, vm_filename):
        self.current_vm_filename = vm_filename

    def build_program_flow_command(self, command):
        if command.command_name == 'label':
            return self.build_label_command(command.label)
        elif command.command_name == 'goto':
            return self.build_goto_command(command.label)
        else:
            return self.build_if_goto_command(command.label)

    def build_label_command(self, label):
        return [
            '({})'.format(
                self.get_label_in_current_function_context(label)
            )
        ]

    def build_goto_command(self, label):
        return [
            '@{}'.format(self.get_label_in_current_function_context(label)),
            'D;JMP',
        ]

    def build_if_goto_command(self, label):
        return [
            # pop top element off stack and store in D register
            '@SP',
            'M=M-1',
            'A=M',
            'D=M',

            # jump to provided label if popped element is true
            '@{}'.format(self.get_label_in_current_function_context(label)),
            'D;JNE',
        ]

    def build_function_command(self, command):
        function_label_command = ['({})'.format(command.function_name)]
        push_0_command = self.push_pop_command_builder.build_push_pop(
            PushPopCommand('push', 'constant', '0')
        )
        # TODO: do this with a loop in the asm?
        initialization = push_0_command * command.num_local_variables

        self.current_function = command.function_name

        return function_label_command + initialization

    def build_call_command(self, command):
        return_address_label = self.get_return_address_label()

        asm_commands = ['// Save return address to stack']
        asm_commands += self.push_pop_command_builder.build_commands_to_push_arbitrary_value(
            return_address_label
        )
        asm_commands += ['']

        for segment in ('LCL', 'ARG', 'THIS', 'THAT'):
            asm_commands += ['// Save {} to stack'.format(segment)]
            asm_commands += self.push_pop_command_builder.build_commands_to_push_pointer(
                segment
            )
            asm_commands += ['']

        asm_commands += [
            # set ARG to be (# of saved segments on stack + # args) behind SP
            '// set ARG pointer',
            '@SP',
            'D=M',

            # 5 is the number of saved slots on the stack between SP and the 
            # caller's pushed arguments (return address, LCL, ARG, THIS, THAT)
            '@{}'.format(5 + command.num_args),
            'D=D-A',
            '@ARG',
            'M=D',
            '',

            # the function def handles pushing the locals onto the stack, which
            # will push LCL ahead of SP
            '// set LCL=SP',
            '@SP',
            'D=M',
            '@LCL',
            'M=D',
            '',

            '// jump to function label',
            '@{}'.format(command.function_name),
            'D;JMP',
        ]

        # store the return address so we can come back
        asm_commands +=['({})'.format(return_address_label)]
        return asm_commands

    def build_return_command(self, command):
        asm_commands = [
            # LCL starts 5 addresses ahead of the return address
            '// store return address in R13',
            '@5',
            'D=A',
            '@LCL',
            'A=M-D',  # A is now the address that contains the return address
            'D=M',
            '@R13',
            'M=D',
            '',

            '// put return value where ARG currently points (will be top of stack)',
            '@SP',
            'A=M-1',
            'D=M',
            '@ARG',
            'A=M',
            'M=D',
            '',

            '// move SP to one after return value we just placed',
            'D=A+1',
            '@SP',
            'M=D',
            '',
        ]

        # order matters since these are all defined relative to the current
        # state of LCL -- so we have to change LCL last
        for register_name in ('THAT', 'THIS', 'ARG', 'LCL'):
            asm_commands += ['// restore {}'.format(register_name)]
            asm_commands += self._build_command_to_restore_saved_state(
                register_name
            )
            asm_commands += ['']

        asm_commands += [
            '// jump to stored return address',
            '@R13',
            'A=M',
            '0;JMP',
            '',
        ]

        return asm_commands

    # maps registers that are saved on stack during a function call (for the
    # previous function context) to their offset before the LCL variables of
    # the current function context
    REGISTER_NAME_TO_LCL_OFFSET = {
        'THAT': 1,
        'THIS': 2,
        'ARG': 3,
        'LCL': 4,
    }

    def _build_command_to_restore_saved_state(self, register_name):
        return [
            '@LCL',
            'D=M',
            '@{}'.format(self.REGISTER_NAME_TO_LCL_OFFSET[register_name]),
            'A=D-A',
            'D=M',
            '@{}'.format(register_name),
            'M=D',
        ]
