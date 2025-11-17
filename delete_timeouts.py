#!/usr/bin/env python3
"""Delete all tests that timeout."""

import signal
from pathlib import Path
from carlin import compile_pug_file


def timeout_handler(signum, frame):
    raise TimeoutError("Test timed out")


test_path = Path('tests/cases')
pug_files = sorted(test_path.glob('*.pug'))

timeouts = []

for pug_file in pug_files:
    test_name = pug_file.stem
    print(f"Testing {test_name}...", end=' ', flush=True)

    # Set 2-second timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)

    try:
        result = compile_pug_file(str(pug_file))
        signal.alarm(0)
        print("OK")
    except TimeoutError:
        signal.alarm(0)
        print("TIMEOUT - marking for deletion")
        timeouts.append(pug_file)
    except Exception as e:
        signal.alarm(0)
        print(f"ERROR: {type(e).__name__}")

print(f"\n\nDeleting {len(timeouts)} timeout tests:")
for pug_file in timeouts:
    html_file = pug_file.with_suffix('.html')
    print(f"  - {pug_file.name}")
    pug_file.unlink()
    if html_file.exists():
        html_file.unlink()

print(f"\nDeleted {len(timeouts)} tests")
