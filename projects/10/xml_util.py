import re
import os
from xml.dom import minidom
from xml.etree import ElementTree

from parsing.parse_node import NonTerminalParseNode


EMPTY_XML_TAG_LINE_RE = '^(?P<indentation>\s*)<(?P<tag>.*?)/>\s*$'


def generate_and_save_token_xml(tokens, jack_file_path):
    token_element_tree = _generate_token_element_tree(tokens)
    output_file_path = _get_token_output_file_path(jack_file_path)
    save_xml_to_file(token_element_tree, output_file_path)


def _generate_token_element_tree(tokens):
    root = ElementTree.Element('tokens')
    for token in tokens:
        element = ElementTree.SubElement(root, token.type)
        element.text = token.value
    return root


def _get_token_output_file_path(jack_file_path):
    jack_file_dir, jack_file_name = os.path.split(jack_file_path)
    output_dir = _get_token_output_dir(jack_file_dir)

    output_file_name = '{jack_file_name}T.xml'.format(
        jack_file_name=jack_file_name[:-5],  # remove .jack
    )
    return os.path.join(output_dir, output_file_name)


def _get_token_output_dir(jack_file_dir):
    output_dir_path = '{}/generated_token_xml/'.format(jack_file_dir)

    # TODO: not the best to do this more than once
    if not os.path.exists(output_dir_path):
        os.mkdir(output_dir_path)
    return output_dir_path


def save_xml_to_file(token_element_tree, output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write(
            format_xml(token_element_tree)
        )


def format_xml(element_tree):
    ugly_xml = ElementTree.tostring(element_tree)
    pretty_xml = minidom.parseString(ugly_xml).toprettyxml()

    # nand2tetris provided comparison xmls for comparison don't have the
    # <?xml version...> tag
    xml_version_line, xml_minus_version = pretty_xml.split('\n', maxsplit=1)

    # it also doesn't like empty tags (i.e. <tag/>) :(
    xml_minus_version_minus_empty_tags = re.sub(
        pattern=EMPTY_XML_TAG_LINE_RE,
        repl=_replace_empty_xml_tag_from_match,
        string=xml_minus_version,
        flags=re.MULTILINE,  # ^ matches new lines, not just start of string
    )

    return xml_minus_version_minus_empty_tags


def _replace_empty_xml_tag_from_match(match):
    groupdict = match.groupdict()
    return '{indentation}<{tag}>\n{indentation}</{tag}>'.format(
        indentation=groupdict['indentation'],
        tag=groupdict['tag'],
    )


def save_parse_tree_to_xml_file(parse_tree_root, jack_file_path):
    xml_element = convert_parse_tree_node_to_xml_element(parse_tree_root)
    output_file_path = _get_output_file_path(jack_file_path)
    save_xml_to_file(xml_element, output_file_path)


def convert_parse_tree_node_to_xml_element(parse_tree_node):
    xml_element = ElementTree.Element(parse_tree_node.grammar_element_name)

    if isinstance(parse_tree_node, NonTerminalParseNode):
        for child_node in parse_tree_node.child_nodes:
            xml_element.append(
                convert_parse_tree_node_to_xml_element(child_node)
            )
    else:
        xml_element.text = parse_tree_node.token.value

    return xml_element


def _get_output_file_path(jack_file_path):
    return '{}_parse_tree.xml'.format(
        jack_file_path[:-5],  # remove .jack
    )
