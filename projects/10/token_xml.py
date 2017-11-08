import os
from xml.dom import minidom
from xml.etree import ElementTree


def generate_and_save_token_xml(tokens, jack_file_path):
    token_element_tree = _generate_token_element_tree(tokens)
    output_file_path = _get_output_file_path(jack_file_path)
    _save_token_xml(token_element_tree, output_file_path)


def _generate_token_element_tree(tokens):
    root = ElementTree.Element('tokens')
    for token in tokens:
        element = ElementTree.SubElement(root, token.token_type)
        element.text = str(token.element)
    return root


def _get_output_file_path(jack_file_path):
    jack_file_dir, jack_file_name = os.path.split(jack_file_path)
    output_dir = _get_output_dir(jack_file_dir)

    output_file_name = '{jack_file_name}T.xml'.format(
        jack_file_name=jack_file_name[:-5],  # remove .jack
    )
    return os.path.join(output_dir, output_file_name)


def _get_output_dir(jack_file_dir):
    output_dir_path = '{}/generated_token_xml/'.format(jack_file_dir)
    
    # TODO: not the best to do this more than once
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)
    return output_dir_path


def _save_token_xml(token_element_tree, output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write(
            _format_xml(token_element_tree)
        )


def _format_xml(element_tree):
    ugly_xml = ElementTree.tostring(element_tree)
    pretty_xml = minidom.parseString(ugly_xml).toprettyxml()
    split_pretty_xml = pretty_xml.split('\n')

    # unfortunately the provided comparison tool doesn't like the xml version
    # tag :-P
    split_pretty_xml_without_metadata = split_pretty_xml[1:]
    return '\n'.join(split_pretty_xml_without_metadata)
