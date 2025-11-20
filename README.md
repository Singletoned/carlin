# Carlin

A Python implementation of PugJS template engine.

## Installation

```bash
pip install -r requirements.txt
pip install -e .  # Install CLI tool
```

## Usage

### Command Line

Compile a Pug file to HTML:

```bash
carlin template.pug                    # Output to stdout
carlin template.pug -o output.html     # Output to file
carlin template.pug --pretty           # Pretty-print HTML
```

### Python API

```python
from carlin import compile_pug

html = compile_pug("div Hello World")
print(html)
```

## Testing

Using the test runner:
```bash
python test_runner.py
```

Or with [just](https://github.com/casey/just):
```bash
just test           # Run all tests
just test-verbose   # Run tests with verbose output
just test-case basic  # Test a specific case
just compare basic    # Compare output with expected
```

## Development

See available commands:
```bash
just --list
```

Common commands:
- `just install` - Install dependencies
- `just test` - Run all tests
- `just clean` - Clean Python cache files
- `just stats` - Show test statistics
