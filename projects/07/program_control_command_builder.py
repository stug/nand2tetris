class ProgramControlCommandBuilder(object):

    def __init__(self):
        # stack of what function we're currently in, used to ensure that labels
        # can be reused across functions without duplication in the resulting
        # assembly. Entering a function pushes onto the stack, exiting pops
        # from it.
        self.function_context = []

    def get_label_in_current_function_context(self, label):
        return '{function}${label}'.format(
            function=self.function_context[-1] if self.function_context else '',
            label=label
        )

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
            'D;JNE'
        ]

    # TODO: This is sort of gross.  Really the command builders should probably
    # just register a mapping of commands they handle to methods that build the
    # asm for those commands.
    def build_function_or_call_command(self, command):
        if command.command_name == 'function':
            return self.build_function_command(command)
        else:
            return self.build_call_command(command)

    def build_function_command(self, command):
        pass

    def build_call_command(self, command):
        pass

    def build_return_command(self, command):
        pass
