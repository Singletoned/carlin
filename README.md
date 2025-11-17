# Carlin

A Python implementation of PugJS template engine.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from carlin import compile_pug

html = compile_pug("div Hello World")
print(html)
```

## Testing

```bash
pytest
```
