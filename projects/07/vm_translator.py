import argparse
import os
import sys

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

    def get_vm_files_in_direcotry(self, path):
        files = os.listdir(path)
        vm_files = [file for file in files if file.endswith('.vm')]
        if not vm_files:
            raise Exception('Provided directory contains no .vm files')
        return vm_files

    def generate_output_filename(self, dir_or_file):
        basename = os.path.basename(dir_or_file)
        basename_without_extension = basename.replace('.vm', '')
        return '{}.asm'.format(basename_without_extension)

    def translate(self):
        with self.codewriter.open():
            for vm_file_path in self.vm_file_paths:
                self.codewriter.set_vm_filename(vm_file_path)
                for command in Parser(vm_file_path).parse():
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
