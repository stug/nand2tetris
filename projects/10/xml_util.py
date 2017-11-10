import re
from xml.dom import minidom
from xml.etree import ElementTree


EMPTY_XML_TAG_LINE_RE = '^(?P<indentation>\s*)<(?P<tag>.*?)/>\s*$'


def save_xml_to_file(token_element_tree, output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write(
            format_xml(token_element_tree)
        )


# TODO: need to change single empty tag to open and close pair
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
