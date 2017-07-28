class CommandParseException(Exception): pass


class Command(object):

    EXPECTED_ARG_LENGTH = 0
    HANDLED_COMMANDS = []

    def __init__(self, command_name, *args):
        self.command_name = command_name
        self.process_args(args)
        self.args = args

    def process_args(self, args):
        if len(args) != self.EXPECTED_ARG_LENGTH:
            raise CommandParseException(
                'Expected {} args'.format(
                    self.EXPECTED_ARG_LENGTH
                )
            )

    def __str__(self):
        return '{command} {args}'.format(
            command=self.command_name,
            args=' '.join(self.args)
        )


# TODO: should subclasses of Command live in their respective command builder
# modules?
class TwoOperandArithmeticCommand(Command):

    HANDLED_COMMANDS = ['add', 'sub', 'and', 'or']


class ComparisonCommand(Command):

    HANDLED_COMMANDS = ['eq', 'gt', 'lt']


class OneOperandArithmeticCommand(Command):

    HANDLED_COMMANDS = ['neg', 'not']


class PushPopCommand(Command):

    EXPECTED_ARG_LENGTH = 2
    HANDLED_COMMANDS = ['push', 'pop']
    MEMORY_SEGMENTS = set([
        'argument', 'local', 'static', 'constant', 'this', 'that', 'pointer',
        'temp'
    ])

    memory_segment = None
    index = None

    def process_args(self, args):
        super(PushPopCommand, self).process_args(args)
        self.memory_segment = args[0]
        if self.memory_segment not in self.MEMORY_SEGMENTS:
            raise CommandParseException('Invalid memory segment')

        if self.command_name == 'pop' and self.memory_segment == 'constant':
            raise CommandParseException("Can't pop to constant!")

        self.index = args[1]


class ProgramFlowCommand(Command):

    EXPECTED_ARG_LENGTH = 1
    HANDLED_COMMANDS = ['label', 'goto', 'if-goto']

    label = None

    def process_args(self, args):
        super(ProgramFlowCommand, self).process_args(args)
        self.label = args[0]


class FunctionCommand(Command):

    EXPECTED_ARG_LENGTH = 2
    HANDLED_COMMANDS = ['function']

    function_name = None
    num_local_variables = None

    def process_args(self, args):
        super(FunctionCommand, self).process_args(args)
        self.function_name = args[0]
        self.num_local_variables = int(args[1])


class CallCommand(Command):

    EXPECTED_ARG_LENGTH = 2
    HANDLED_COMMANDS = ['call']

    function_name = None
    num_args = None

    def process_args(self, args):
        super(CallCommand, self).process_args(args)
        self.function_name = args[0]
        self.num_args = int(args[1])


class ReturnCommand(Command):

    HANDLED_COMMANDS = ['return']


# could do this with a metaclass, but blech to that
COMMAND_TO_TYPE = {}
for command_type in [
    TwoOperandArithmeticCommand,
    ComparisonCommand,
    OneOperandArithmeticCommand,
    PushPopCommand,
    ProgramFlowCommand,
    FunctionCommand,
    CallCommand,
    ReturnCommand,
]:
    COMMAND_TO_TYPE.update({
        handled_command: command_type
        for handled_command in command_type.HANDLED_COMMANDS
    })
