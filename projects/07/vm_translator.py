import argparse
import os

from code_writer import CodeWriter
from parser import Parser


class VMTranslator(object):

    def __init__(self, dir_or_file):
        self.vm_file_paths = self.get_vm_files_from_path(dir_or_file)

        output_filename = self.generate_output_filename(dir_or_file)
        self.codewriter = CodeWriter(output_filename)

    def get_vm_files_from_path(self, path):
        if os.path.isdir(path):
            return self.get_vm_files_in_directory(path)
        elif os.path.isfile(path):
            return [path]
        else:
            raise Exception('Please provide a valid file or directory')

    def get_vm_files_in_directory(self, path):
        filenames = os.listdir(path)
        dirname = os.path.dirname(path)
        vm_files = [
            os.path.join(dirname, filename)
            for filename in filenames if filename.endswith('.vm')
        ]
        if not vm_files:
            raise Exception('Provided directory contains no .vm files')
        return vm_files

    def generate_output_filename(self, dir_or_file):
        dirname, basename = os.path.split(dir_or_file)

        if os.path.isdir(dir_or_file):
            basename = dirname.split('/')[-1]
        else:
            basename = basename.replace('.vm', '')

        return os.path.join(dirname, '{}.asm'.format(basename))

    def translate(self):
        with self.codewriter.open():
            for vm_file_path in self.vm_file_paths:
                base_vm_filename = os.path.basename(vm_file_path)
                self.codewriter.set_vm_filename(base_vm_filename)
                for command in Parser(vm_file_path).yield_parsed_commands():
                    self.codewriter.translate_and_write_vm_command(command)


def build_argparser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'file_or_directory',
        help='vm file or directory containing vm files'
    )
    return argparser


if __name__ == '__main__':
    args = build_argparser().parse_args()
    VMTranslator(args.file_or_directory).translate()
