#!/usr/bin/env python3
"""Find which test is hanging."""

import os
import sys
import signal
from pathlib import Path
from carlin import compile_pug_file


def timeout_handler(signum, frame):
    raise TimeoutError("Test timed out")


test_path = Path('tests/cases')
pug_files = sorted(test_path.glob('*.pug'))

for pug_file in pug_files:
    test_name = pug_file.stem
    print(f"Testing {test_name}...", end=' ', flush=True)

    # Set 2-second timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)

    try:
        result = compile_pug_file(str(pug_file))
        signal.alarm(0)  # Cancel alarm
        print("OK")
    except TimeoutError:
        signal.alarm(0)
        print("TIMEOUT!")
        break
    except Exception as e:
        signal.alarm(0)
        print(f"ERROR: {type(e).__name__}")
