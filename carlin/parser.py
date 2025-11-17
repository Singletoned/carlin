"""Pug parser using Lark."""

from lark import Lark
from lark.indenter import Indenter
from pathlib import Path


class PugIndenter(Indenter):
    NL_type = '_NEWLINE'
    OPEN_PAREN_types = []
    CLOSE_PAREN_types = []
    INDENT_type = '_INDENT'
    DEDENT_type = '_DEDENT'
    tab_len = 2


def create_parser():
    """Create and return a Lark parser for Pug syntax."""
    grammar_path = Path(__file__).parent / "grammar.lark"
    with open(grammar_path, 'r') as f:
        grammar = f.read()

    parser = Lark(
        grammar,
        parser='lalr',
        postlex=PugIndenter(),
        propagate_positions=True,
        maybe_placeholders=True
    )
    return parser


def parse_pug(source: str):
    """Parse Pug source code and return AST."""
    parser = create_parser()
    return parser.parse(source)
