from commands import COMMAND_TO_TYPE


class Parser(object):

    COMMENT_DELIMITER = '//'

    def __init__(self, vm_file_path):
        self.vm_file_path = vm_file_path

    def parse(self):
        with open(self.vm_file_path, 'r') as vm_file:
            for line in vm_file:
                command = self.parse_line(line)
                if command:
                    yield command

    def parse_line(self, line):
        tokens = self.tokenize(line)
        if tokens:
            return self.categorize(tokens)
        else:
            return None

    def tokenize(self, line):
        line = self.strip_comment(line)
        return line.split()

    def strip_comment(self, line):
        comment_start_index = line.find(self.COMMENT_DELIMITER)
        if comment_start_index != -1:
            return line[:comment_start_index]
        else:
            return line

    def categorize(self, tokens):
        command = tokens[0]
        return COMMAND_TO_TYPE[command](*tokens)
