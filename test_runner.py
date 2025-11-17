#!/usr/bin/env python3
"""Test runner for Carlin Pug compiler."""

import os
import sys
from pathlib import Path
from carlin import compile_pug_file
import re


def normalize_html(html):
    """Normalize HTML for comparison."""
    # Remove extra whitespace
    html = re.sub(r'>\s+<', '><', html)
    html = re.sub(r'\s+', ' ', html)
    html = html.strip()
    return html


def run_tests(test_dir='tests/cases', verbose=False):
    """Run all Pug test cases."""
    test_path = Path(test_dir)
    pug_files = sorted(test_path.glob('*.pug'))

    passed = 0
    failed = 0
    errors = 0

    print(f"Running {len(pug_files)} test cases...\n")

    for pug_file in pug_files:
        test_name = pug_file.stem
        html_file = pug_file.with_suffix('.html')

        if not html_file.exists():
            if verbose:
                print(f"⊘ {test_name}: No expected HTML file")
            continue

        print(f"Testing {test_name}...", flush=True)  # Progress indicator

        try:
            # Compile Pug
            actual_html = compile_pug_file(str(pug_file))

            # Read expected HTML
            with open(html_file, 'r', encoding='utf-8') as f:
                expected_html = f.read()

            # Normalize both
            actual_normalized = normalize_html(actual_html)
            expected_normalized = normalize_html(expected_html)

            # Compare
            if actual_normalized == expected_normalized:
                passed += 1
                if verbose:
                    print(f"✓ {test_name}")
            else:
                failed += 1
                print(f"✗ {test_name}")
                if verbose:
                    print(f"  Expected: {expected_normalized[:100]}...")
                    print(f"  Actual:   {actual_normalized[:100]}...")
                    print()

        except Exception as e:
            errors += 1
            print(f"E {test_name}: {type(e).__name__}: {str(e)[:80]}")
            if verbose:
                import traceback
                traceback.print_exc()
                print()

    # Summary
    total = passed + failed + errors
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed, {errors} errors out of {total} tests")
    print(f"Success rate: {passed/total*100:.1f}%" if total > 0 else "No tests run")

    return passed, failed, errors


if __name__ == '__main__':
    verbose = '-v' in sys.argv or '--verbose' in sys.argv
    passed, failed, errors = run_tests(verbose=verbose)
    sys.exit(0 if failed == 0 and errors == 0 else 1)
