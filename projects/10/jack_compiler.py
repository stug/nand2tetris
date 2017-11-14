import argparse
import os
from enum import Enum

from parsing.jack_non_terminals import Class
from parsing.parse_node import ParseException
from parsing.token_proxy import TokenProxy
from tokenizer import Tokenizer
from xml_util import convert_parse_tree_node_to_xml_element
from xml_util import format_xml
from xml_util import generate_and_save_token_xml
from xml_util import save_parse_tree_to_xml_file


class OutputType(Enum):
    TOKEN_XML = 1
    XML = 2
    VM_CODE = 3


def compile_files(file_or_directory, output_type):
    jack_file_paths = _get_jack_files_from_path(file_or_directory)
    for jack_file_path in jack_file_paths:
        _compile_file(jack_file_path, output_type)


def _compile_file(jack_file_path, output_type):
    tokens = Tokenizer(jack_file_path).yield_tokens()
    if output_type == OutputType.TOKEN_XML:
        generate_and_save_token_xml(tokens, jack_file_path)
    elif output_type == OutputType.XML:
        _compile_tokens_to_xml(tokens, jack_file_path)


def _compile_tokens_to_xml(tokens, jack_file_path):
    token_proxy = TokenProxy(list(tokens))
    parse_tree_root = Class()

    try:
        parse_tree_root.attempt_parse(token_proxy)
    except Exception as e:
        print('Encountered issue in {}'.format(jack_file_path))
        xml_element = convert_parse_tree_node_to_xml_element(parse_tree_root)
        print(format_xml(xml_element))
        raise

    save_parse_tree_to_xml_file(parse_tree_root, jack_file_path)


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

    output_type_group = argparser.add_mutually_exclusive_group(required=True)
    output_type_group.add_argument(
        '--token-xml',
        help='output token xml',
        action='store_const',
        dest='output_type',
        const=OutputType.TOKEN_XML,
    )
    output_type_group.add_argument(
        '--xml',
        help='output parse tree xml',
        action='store_const',
        dest='output_type',
        const=OutputType.XML,
    )
    return argparser


if __name__ == '__main__':
    args = build_argparser().parse_args()
    compile_files(
        args.file_or_directory,
        output_type=args.output_type,
    )
