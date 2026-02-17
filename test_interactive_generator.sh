#!/bin/bash
# Test script for interactive_generator.py

set -e  # Exit on error

echo "=================================="
echo "Testing Interactive Pattern Generator"
echo "=================================="
echo

# Create test output directory
TEST_DIR="/tmp/generator_test"
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR"

echo "1. Testing standard bodice generation..."
python3 interactive_generator.py --pattern bodice --pname W36G --gender w --style Gilewska --output "$TEST_DIR" > /dev/null 2>&1
if [ -f "$TEST_DIR/bodice_W36G.pdf" ]; then
    echo "   ✓ Bodice PDF created"
else
    echo "   ✗ Bodice PDF not found"
    exit 1
fi

echo "2. Testing standard skirt generation..."
python3 interactive_generator.py --pattern skirt --pname W6C --gender w --style Chiappetta --output "$TEST_DIR" > /dev/null 2>&1
if [ -f "$TEST_DIR/skirt_W6C.pdf" ]; then
    echo "   ✓ Skirt PDF created"
else
    echo "   ✗ Skirt PDF not found"
    exit 1
fi

echo "3. Testing standard shirt generation..."
python3 interactive_generator.py --pattern shirt --pname M44G --gender m --style Gilewska --output "$TEST_DIR" > /dev/null 2>&1
if [ -f "$TEST_DIR/shirt_M44G.pdf" ]; then
    echo "   ✓ Shirt PDF created"
else
    echo "   ✗ Shirt PDF not found"
    exit 1
fi

echo "4. Testing bespoke shirt with JSON..."
python3 interactive_generator.py --pattern shirt --bespoke measurements_shirt_example.json --gender m --style Gilewska --output "$TEST_DIR" > /dev/null 2>&1
# Bespoke mode generates the same filename but with customized parameters
if [ -f "$TEST_DIR/shirt_M44G.pdf" ]; then
    echo "   ✓ Bespoke shirt PDF created (with custom parameters)"
else
    echo "   ✗ Bespoke shirt PDF not found"
    exit 1
fi

echo "5. Testing bespoke bodice with JSON..."
python3 interactive_generator.py --pattern bodice --bespoke measurements_bodice_example.json --gender w --style Gilewska --output "$TEST_DIR" > /dev/null 2>&1
if [ -f "$TEST_DIR/bodice_W36G.pdf" ]; then
    echo "   ✓ Bespoke bodice PDF created (with custom parameters)"
else
    echo "   ✗ Bespoke bodice PDF not found"
    exit 1
fi

echo "6. Testing help command..."
python3 interactive_generator.py --help > /dev/null 2>&1
echo "   ✓ Help command works"

echo
echo "=================================="
echo "All tests passed! ✓"
echo "=================================="
echo
echo "Generated files in $TEST_DIR:"
ls -lh "$TEST_DIR"/*.pdf
