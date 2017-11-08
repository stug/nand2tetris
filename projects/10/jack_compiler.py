import argparse
import os
from enum import Enum

from tokenizer import Tokenizer
from token_xml import generate_and_save_token_xml


class OutputType(Enum):
    TOKEN_XML = 1
    XML = 2
    VM_CODE = 3


def compile_files(file_or_directory, output_type):
    jack_file_paths = _get_jack_files_from_path(file_or_directory)
    for jack_file_path in jack_file_paths:
        tokens = Tokenizer(jack_file_path).yield_tokens()
        if output_type == OutputType.TOKEN_XML:
            generate_and_save_token_xml(tokens, jack_file_path)


def _get_jack_files_from_path(path):
    if os.path.isdir(path):
        return _get_jack_files_in_directory(path)
    elif os.path.isfile(path) and path.endswith('.jack'):
        return [path]
    else:
        raise Exception('Please provide a valid file or directory')


def _get_jack_files_in_directory(directory_path):
    filenames = os.listdir(directory_path)
    dirname = os.path.dirname(directory_path)
    jack_files = [
        os.path.join(dirname, filename)
        for filename in filenames if filename.endswith('.jack')
    ]
    if not jack_files:
        raise Exception('Provided directory contains no .jack files')
    return jack_files


def build_argparser():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        'file_or_directory',
        help='jack file or directory containing jack files',
    )

    output_type_group = argparser.add_mutually_exclusive_group()
    output_type_group.add_argument(
        '--token-xml',
        help='output token xml',
        action='store_const',
        dest='output_type',
        const=OutputType.TOKEN_XML,
    )
    return argparser


if __name__ == '__main__':
    args = build_argparser().parse_args()
    compile_files(
        args.file_or_directory,
        output_type=args.output_type,
    )
