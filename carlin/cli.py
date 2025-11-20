"""Command-line interface for Carlin."""

import sys
import argparse
from pathlib import Path
from .compiler import compile_pug_file


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Carlin - Compile Pug templates to HTML',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  carlin template.pug              # Output to stdout
  carlin template.pug -o out.html  # Output to file
  carlin input.pug --pretty        # Pretty-print HTML
        """
    )

    parser.add_argument(
        'input',
        help='Input Pug file to compile'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output HTML file (default: stdout)',
        default=None
    )

    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print the HTML output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Carlin 0.1.0'
    )

    args = parser.parse_args()

    # Check if input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    if not input_path.suffix == '.pug':
        print(f"Warning: File '{args.input}' does not have .pug extension", file=sys.stderr)

    # Compile the Pug file
    try:
        html = compile_pug_file(str(input_path), pretty=args.pretty)
    except Exception as e:
        print(f"Error compiling {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    # Output the result
    if args.output:
        output_path = Path(args.output)
        try:
            output_path.write_text(html, encoding='utf-8')
            print(f"Compiled {args.input} -> {args.output}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing to {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Output to stdout
        print(html)


if __name__ == '__main__':
    main()
