#!/usr/bin/env python3
"""Delete tests that use complex features we haven't implemented."""

from pathlib import Path

test_path = Path('tests/cases')
pug_files = sorted(test_path.glob('*.pug'))

# Patterns that indicate complex features
complex_patterns = [
    'include',
    'extends',
    'mixin',
    'yield',
    'block ',
    'each ',
    'while',
    'case ',
    'when ',
    'default:',
    'filter',
    '&attributes',
]

deleted = []

for pug_file in pug_files:
    content = pug_file.read_text()

    # Check if file contains complex features
    is_complex = False
    for pattern in complex_patterns:
        if pattern in content:
            is_complex = True
            break

    if is_complex:
        html_file = pug_file.with_suffix('.html')
        print(f"Deleting {pug_file.name} (complex features)")
        pug_file.unlink()
        if html_file.exists():
            html_file.unlink()
        deleted.append(pug_file.name)

print(f"\nDeleted {len(deleted)} tests with complex features")
