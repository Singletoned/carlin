"""Pug to HTML compiler."""

import re
from lxml import etree
from .simple_parser import parse_pug, TagNode, TextNode, CommentNode


def is_valid_xml_name(name: str) -> bool:
    """Check if a name is a valid XML name."""
    if not name:
        return False
    # XML names must start with a letter, underscore, or colon
    # and contain only letters, digits, hyphens, underscores, colons, or periods
    # We'll be more restrictive and follow HTML attribute rules
    pattern = r'^[a-zA-Z_:][-a-zA-Z0-9_:.]*$'
    return re.match(pattern, name) is not None


def node_to_html(node) -> etree.Element:
    """Convert a node to an lxml Element."""
    if isinstance(node, TagNode):
        # Create element
        elem = etree.Element(node.name)

        # Add ID
        if node.id:
            elem.set('id', node.id)

        # Add classes
        if node.classes:
            elem.set('class', ' '.join(node.classes))

        # Add attributes
        for key, value in node.attributes.items():
            # Skip invalid XML attribute names
            if not is_valid_xml_name(key):
                continue
            elem.set(key, str(value))

        # Add text content
        if node.text:
            elem.text = node.text

        # Add children
        for child in node.children:
            child_elem = node_to_html(child)
            if child_elem is not None:
                elem.append(child_elem)

        return elem

    elif isinstance(node, TextNode):
        # Text nodes don't create elements - they should be added to parent
        return None

    elif isinstance(node, CommentNode):
        # For now, ignore comments
        return None

    return None


def compile_pug(source: str, pretty: bool = False) -> str:
    """
    Compile Pug source code to HTML.

    Args:
        source: Pug source code
        pretty: Whether to pretty-print the HTML

    Returns:
        HTML string
    """
    # Parse
    nodes = parse_pug(source)

    # Convert to HTML
    html_parts = []
    for node in nodes:
        elem = node_to_html(node)
        if elem is not None:
            html_str = etree.tostring(elem, encoding='unicode', method='html')
            html_parts.append(html_str)

    html = ''.join(html_parts)

    # Pretty print if requested
    if pretty:
        try:
            parser = etree.HTMLParser()
            tree = etree.fromstring(html, parser)
            html = etree.tostring(tree, encoding='unicode', pretty_print=True, method='html')
        except:
            pass

    return html


def compile_pug_file(filepath: str, pretty: bool = False) -> str:
    """
    Compile a Pug file to HTML.

    Args:
        filepath: Path to Pug file
        pretty: Whether to pretty-print the HTML

    Returns:
        HTML string
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    return compile_pug(source, pretty=pretty)
