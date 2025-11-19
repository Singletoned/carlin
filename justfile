# Carlin - Pug template engine for Python

# List available recipes
default:
    @just --list

# Install dependencies
install:
    pip install -r requirements.txt

# Run all tests
test:
    python test_runner.py

# Run tests with verbose output
test-verbose:
    python test_runner.py -v

# Run a specific test case
test-case case:
    python -c "from carlin import compile_pug_file; print(compile_pug_file('tests/cases/{{case}}.pug'))"

# Compare test output with expected
compare case:
    @echo "Actual output:"
    @python -c "from carlin import compile_pug_file; print(compile_pug_file('tests/cases/{{case}}.pug'))"
    @echo "\nExpected output:"
    @cat tests/cases/{{case}}.html

# Clean Python cache files
clean:
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete

# Format code (if black is installed)
format:
    black carlin/ test_runner.py || echo "Install black with: pip install black"

# Run the example from README
example:
    python -c "from carlin import compile_pug; print(compile_pug('div Hello World'))"

# Show test statistics
stats:
    @echo "Test files remaining: $(ls tests/cases/*.pug 2>/dev/null | wc -l)"
    @echo "Test results:"
    @python test_runner.py 2>&1 | grep "Results:"
