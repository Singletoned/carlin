"""Simple custom parser for Pug that handles indentation manually."""

import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Node:
    """Base class for AST nodes."""
    pass


@dataclass
class TagNode(Node):
    """Represents an HTML tag."""
    name: str
    attributes: Dict[str, str]
    classes: List[str]
    id: Optional[str]
    text: Optional[str]
    children: List[Node]
    indent: int


@dataclass
class TextNode(Node):
    """Represents plain text."""
    text: str
    indent: int


@dataclass
class CommentNode(Node):
    """Represents a comment."""
    text: str
    buffered: bool
    indent: int


class PugParser:
    """Simple Pug parser that handles basic syntax."""

    def __init__(self):
        self.lines = []
        self.current = 0

    def parse(self, source: str) -> List[Node]:
        """Parse Pug source into AST."""
        # Split into lines and track indentation
        self.lines = []
        for line in source.split('\n'):
            if not line.strip():
                continue  # Skip blank lines
            indent = len(line) - len(line.lstrip())
            content = line.strip()
            self.lines.append((indent, content))

        self.current = 0
        return self._parse_nodes(0)

    def _parse_nodes(self, min_indent: int) -> List[Node]:
        """Parse nodes at the current indentation level."""
        nodes = []

        while self.current < len(self.lines):
            indent, content = self.lines[self.current]

            if indent < min_indent:
                break

            if indent > min_indent:
                self.current += 1
                continue

            node = self._parse_line(indent, content)
            if node:
                nodes.append(node)

            self.current += 1

            # Check for children
            if self.current < len(self.lines):
                next_indent, _ = self.lines[self.current]
                if next_indent > indent:
                    children = self._parse_nodes(next_indent)
                    if isinstance(node, TagNode):
                        node.children = children

        return nodes

    def _parse_line(self, indent: int, content: str) -> Optional[Node]:
        """Parse a single line."""
        if not content:
            return None

        # Comments
        if content.startswith('//'):
            buffered = not content.startswith('//- ')
            text = content[2:].strip() if buffered else content[4:].strip()
            return CommentNode(text=text, buffered=buffered, indent=indent)

        # Doctype (ignore for now)
        if content.startswith('doctype'):
            return None

        # Code lines (ignore for now)
        if content.startswith('-') or content.startswith('='):
            return None

        # Tags
        return self._parse_tag(indent, content)

    def _parse_tag(self, indent: int, content: str) -> Optional[TagNode]:
        """Parse a tag line."""
        # Extract tag name, classes, id, attributes, and text
        name = 'div'  # Default
        classes = []
        tag_id = None
        attributes = {}
        text = None

        pos = 0

        # Parse tag name
        if content[0].isalpha():
            match = re.match(r'([a-zA-Z][\w:-]*)', content)
            if match:
                name = match.group(1)
                pos = match.end()

        # Parse classes and IDs
        while pos < len(content) and content[pos] in '.#':
            if content[pos] == '.':
                match = re.match(r'\.([a-zA-Z][\w-]*)', content[pos:])
                if match:
                    classes.append(match.group(1))
                    pos += match.end()
            elif content[pos] == '#':
                match = re.match(r'#([a-zA-Z][\w-]*)', content[pos:])
                if match:
                    tag_id = match.group(1)
                    pos += match.end()

        # Parse attributes
        if pos < len(content) and content[pos] == '(':
            # Find matching closing paren
            paren_count = 1
            attr_start = pos + 1
            pos += 1
            while pos < len(content) and paren_count > 0:
                if content[pos] == '(':
                    paren_count += 1
                elif content[pos] == ')':
                    paren_count -= 1
                pos += 1

            attr_str = content[attr_start:pos-1]
            attributes = self._parse_attributes(attr_str)

        # Parse text content
        if pos < len(content):
            text_part = content[pos:].strip()
            if text_part:
                text = text_part

        return TagNode(
            name=name,
            attributes=attributes,
            classes=classes,
            id=tag_id,
            text=text,
            children=[],
            indent=indent
        )

    def _parse_attributes(self, attr_str: str) -> Dict[str, str]:
        """Parse attribute string."""
        attributes = {}

        if not attr_str.strip():
            return attributes

        # Simple attribute parsing (handles most common cases)
        # Split by comma or space, but not within quotes
        parts = []
        current = ''
        in_quote = False
        quote_char = None

        for char in attr_str:
            if char in ('"', "'") and (not in_quote or char == quote_char):
                in_quote = not in_quote
                quote_char = char if in_quote else None
                current += char
            elif char in (',', ' ') and not in_quote:
                if current.strip():
                    parts.append(current.strip())
                current = ''
            else:
                current += char

        if current.strip():
            parts.append(current.strip())

        # Parse each attribute
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Remove quotes
                if value and value[0] in ('"', "'"):
                    value = value[1:-1]

                # Handle expressions (simplified - just use the value)
                if value.startswith('(') and value.endswith(')'):
                    value = value[1:-1].strip()
                    # For boolean expressions like (1) ? 1 : 0, just output the first option
                    if '?' in value:
                        value = value.split('?')[1].split(':')[0].strip()

                attributes[key] = value
            else:
                # Boolean attribute
                key = part.strip()
                if key:
                    attributes[key] = key

        return attributes


def parse_pug(source: str) -> List[Node]:
    """Parse Pug source code."""
    parser = PugParser()
    return parser.parse(source)
