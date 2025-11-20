"""Pug to HTML compiler."""

import re
from lxml import etree
from .simple_parser import parse_pug, TagNode, TextNode, CommentNode, DoctypeNode


def is_valid_xml_name(name: str) -> bool:
    """Check if a name is a valid XML name."""
    if not name:
        return False
    # XML names must start with a letter, underscore, or colon
    # and contain only letters, digits, hyphens, underscores, colons, or periods
    # We'll be more restrictive and follow HTML attribute rules
    pattern = r'^[a-zA-Z_:][-a-zA-Z0-9_:.]*$'
    return re.match(pattern, name) is not None


def node_to_html_string(node) -> str:
    """Convert a node to an HTML string."""
    if isinstance(node, TagNode):
        # Void/self-closing elements in HTML5
        void_elements = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr'
        }

        # Build opening tag
        tag_parts = [f'<{node.name}']

        # Add ID
        if node.id:
            tag_parts.append(f' id="{node.id}"')

        # Add classes
        if node.classes:
            tag_parts.append(f' class="{" ".join(node.classes)}"')

        # Add attributes
        for key, value in node.attributes.items():
            # Skip invalid XML attribute names
            if not is_valid_xml_name(key):
                continue

            # Boolean attributes (when value equals key name)
            if value == key:
                tag_parts.append(f' {key}')
            else:
                tag_parts.append(f' {key}="{value}"')

        # Handle self-closing tags or void elements
        if node.self_closing:
            tag_parts.append('/>')
            return ''.join(tag_parts)
        elif node.name.lower() in void_elements:
            tag_parts.append('>')
            return ''.join(tag_parts)

        tag_parts.append('>')
        opening_tag = ''.join(tag_parts)

        # Add text content and children
        content_parts = []
        if node.text:
            content_parts.append(node.text)

        for child in node.children:
            child_html = node_to_html_string(child)
            if child_html:
                content_parts.append(child_html)

        # Closing tag
        closing_tag = f'</{node.name}>'

        return opening_tag + ''.join(content_parts) + closing_tag

    elif isinstance(node, TextNode):
        return node.text

    elif isinstance(node, CommentNode):
        # For now, ignore comments
        return ''

    return ''


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
        if isinstance(node, DoctypeNode):
            # Handle doctype declarations
            if node.doctype_str == 'html':
                html_parts.append('<!DOCTYPE html>')
            else:
                html_parts.append(f'<!DOCTYPE {node.doctype_str}>')
        else:
            html_str = node_to_html_string(node)
            if html_str:
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
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        source = f.read()
    return compile_pug(source, pretty=pretty)
