from commands import PushPopCommand


class ProgramControlCommandBuilder(object):

    def __init__(self, push_pop_command_builder):
        # having access to push pop commands simplifies function calling
        self.push_pop_command_builder = push_pop_command_builder

        self.current_vm_filename = None

        # stack of what function we're currently in, used to ensure that labels
        # can be reused across functions without duplication in the resulting
        # assembly. Entering a function pushes onto the stack, exiting pops
        # from it.
        self.function_context = []

    def get_label_in_current_function_context(self, label):
        return '{function}${label}'.format(
            function=self.function_context[-1] if self.function_context else '',
            label=label,
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
        function_name = self._get_qualified_function_name(command.function_name)
        function_label_command = ['({})'.format(function_name)]
        push_0_command = self.push_pop_command_builder.build_push_pop(
            PushPopCommand('push', 'constant', '0')
        )
        # TODO: do this with a loop in the asm?
        initialization = push_0_command * command.num_local_variables

        self.function_context.append(function_name)
        return function_label_command + initialization

    def _get_qualified_function_name(self, function_name):
        return '{vm_filename}.{function_name}'.format(
            vm_filename=self.current_vm_filename,
            function_name=function_name,
        )

    def build_call_command(self, command):
        pass

    def build_return_command(self, command):
        asm_commands = [
            # LCL starts 5 addresses ahead of the return address, so determine
            # the return address and store it in R13
            '@5',
            'D=A',
            '@LCL',
            'A=M-D',  # A is now the address that contains the return address
            'D=M',
            '@R13',
            'M=D',

            # What is currently ARG will be the top of the stack after we
            # return, so put the pushed return value there
            '@SP',
            'A=M-1',
            'D=M',
            '@ARG',
            'A=M',
            'M=D',

            # And move the stack pointer to 1 after the return value we just
            # placed
            'D=A+1',
            '@SP',
            'M=D',
        ]

        # order matters since these are all defined relative to the current
        # state of LCL -- so we have to change LCL last
        for register_name in ('THAT', 'THIS', 'ARG', 'LCL'):
            asm_commands += self._build_command_to_restore_saved_state(
                register_name
            )

        asm_commands += [
            # jump to the stored return address
            '@R13',
            'A=M',
            '0;JMP',
        ]

        self.function_context.pop()
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
