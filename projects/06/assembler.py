import sys

from c_command_builder import CCommandBuilder
from symbol_table import SymbolTable
from util import base10_to_binary
from util import CommandType


class Assembler(object):

    WHITESPACE_CHARACTERS = ['\n', '\t', '\r', ' ']
    COMMENT_MARKER = '//'

    def __init__(self, filename):
        self.filename = filename
        self.next_output_line_num = 0
        self.symbol_table = SymbolTable()

        # TODO: it would be great if this could be defined globally instead of
        # in the class init
        self.command_type_to_code_generator = {
            CommandType.A_COMMAND: self.build_a_command,
            CommandType.C_COMMAND: CCommandBuilder.build_c_command,
        }

    def assemble(self):
        with open(self.filename, 'r') as asm_file:
            self.iter_file(asm_file, self.maybe_add_label_symbol)
            self.iter_file(asm_file, self.generate_code_for_line)

    def iter_file(self, asm_file, method):
        asm_file.seek(0)
        next_output_line_num = 0
        for line in asm_file:
            line = self.sanitize_line(line)
            command_type = self.categorize_line(line)
            if not command_type:
                continue

            method(line, command_type, next_output_line_num)

            if self.should_increment_line_num(command_type):
                next_output_line_num += 1

    def categorize_line(self, line):
        if not line:
            return None

        if line[0] == '@':
            return CommandType.A_COMMAND
        elif line[0] == '(':
            return CommandType.LABEL
        else:
            return CommandType.C_COMMAND

    def sanitize_line(self, line):
        line = self.strip_comment(line)
        line = self.strip_whitespace(line)
        if line:
            return line

    def strip_comment(self, line):
        comment_start_index = line.find(self.COMMENT_MARKER)
        if comment_start_index != -1:
            return line[:comment_start_index]
        return line

    def strip_whitespace(self, line):
        for whitespace_character in self.WHITESPACE_CHARACTERS:
            line = line.replace(whitespace_character, '')
        return line

    def should_increment_line_num(self, command_type):
        return command_type in self.command_type_to_code_generator.keys()

    def maybe_add_label_symbol(self, sanitized_line, command_type, line_num):
        if command_type != CommandType.LABEL:
            return
        label_symbol = sanitized_line[1:-1]
        if self.is_symbol(label_symbol):
            self.symbol_table.add_label_symbol(label_symbol, line_num)
        else:
            raise Exception('Labels must be alphanumeric')

    def maybe_add_variable_symbol(self, sanitized_line, line_num):
        variable_symbol = self.extract_value_from_a_command(sanitized_line)
        if self.is_symbol(variable_symbol):
            self.symbol_table.maybe_add_variable_symbol(variable_symbol)

    def extract_value_from_a_command(self, a_command):
        return a_command[1:]

    def is_symbol(self, string):
        try:
            int(string)
        except ValueError:
            return True
        return False

    def generate_code_for_line(self, line, command_type, line_num):
        if command_type == CommandType.LABEL:
            return

        output_line = self.command_type_to_code_generator[command_type](line)
        print output_line

    def build_a_command(self, sanitized_line):
        value = self.extract_value_from_a_command(sanitized_line)
        if self.is_symbol(value):
            address = self.symbol_table.get_or_add_variable_symbol(value)
        else:
            address =  base10_to_binary(value)

        return '0{}'.format(address.zfill(15))


if __name__ == '__main__':
    Assembler(sys.argv[1]).assemble()
