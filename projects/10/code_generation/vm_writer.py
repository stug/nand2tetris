from contextlib import contextmanager


symbol_kind_to_vm_memory_segment = {
    'static': 'static',
    'field': 'this',
    'var': 'local',
    'arg': 'argument',
}


class VmWriter:

    def __init__(self, output_filename):
        self.output_filename = output_filename
        self.output_file = None

    @contextmanager
    def open(self):
        with open(self.output_filename, 'w') as self.output_file:
            yield self

    def write_push(self, segment, index):
        self.output_file.write('push {segment} {index}\n'.format(
            segment=segment,
            index=str(index),
        ))

    def write_push_from_symbol(self, symbol_info):
        self.write_push(
            segment=symbol_kind_to_vm_memory_segment[symbol_info.kind],
            index=symbol_info.offset,
        )

    def write_pop(self, segment, index):
        self.output_file.write('pop {segment} {index}\n'.format(
            segment=segment,
            index=str(index),
        ))

    def write_pop_to_symbol(self, symbol_info):
        self.write_pop(
            segment=symbol_kind_to_vm_memory_segment[symbol_info.kind],
            index=symbol_info.offset,
        )

    def write_arithmetic(self, command):
        self.output_file.write('{}\n'.format(command))

    def write_label(self, label):
        self.output_file.write('label {label}\n'.format(label=label))

    def write_goto(self, label):
        self.output_file.write('goto {label}\n'.format(label=label))

    def write_ifgoto(self, label):
        self.output_file.write('if-goto {label}\n'.format(label=label))

    def write_call(self, function_name, num_args):
        self.output_file.write('call {function_name} {num_args}\n'.format(
            function_name=function_name,
            num_args=num_args,
        ))

    def write_function(self, name, num_locals):
        self.output_file.write('\nfunction {name} {num_locals}\n'.format(
            name=name,
            num_locals=num_locals,
        ))

    def write_return(self):
        self.output_file.write('return\n')

    def write_newline(self):
        self.output_file.write('\n')
