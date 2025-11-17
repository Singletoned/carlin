"""Carlin - A Python implementation of PugJS template engine."""

from .compiler import compile_pug, compile_pug_file

__version__ = "0.1.0"
__all__ = ["compile_pug", "compile_pug_file"]
