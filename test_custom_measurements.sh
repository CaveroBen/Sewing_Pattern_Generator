#!/bin/bash
set -e

echo "=========================================="
echo "Testing Custom Measurements Feature"
echo "=========================================="
echo

# Test 1: Extract standard measurements
echo "Test 1: Extract standard measurements for W36G"
python3 extract_measurements.py --pname W36G --gender w --output /tmp/test_W36G.json
if [ -f /tmp/test_W36G.json ]; then
    echo "✓ Standard measurements extracted"
else
    echo "✗ Failed to extract measurements"
    exit 1
fi
echo

# Test 2: Extract men's size
echo "Test 2: Extract standard measurements for M44G"
python3 extract_measurements.py --pname M44G --gender m --output /tmp/test_M44G.json
if [ -f /tmp/test_M44G.json ]; then
    echo "✓ Men's measurements extracted"
else
    echo "✗ Failed to extract men's measurements"
    exit 1
fi
echo

# Test 3: Generate with custom measurements
echo "Test 3: Generate bodice with custom measurements"
python3 interactive_generator.py --pattern bodice --bespoke /tmp/test_W36G.json --gender w --style Gilewska --output /tmp/test_output 2>&1 | grep -E "(CUSTOM|Pattern saved)"
if [ -f /tmp/test_output/custom_bodice_W36G.pdf ]; then
    echo "✓ Custom bodice generated"
else
    echo "✗ Failed to generate custom bodice"
    exit 1
fi
echo

# Test 4: Generate men's shirt with custom measurements
echo "Test 4: Generate shirt with custom measurements"
python3 interactive_generator.py --pattern shirt --bespoke /tmp/test_M44G.json --gender m --style Gilewska --output /tmp/test_output 2>&1 | grep -E "(CUSTOM|Pattern saved)"
if [ -f /tmp/test_output/custom_shirt_M44G.pdf ]; then
    echo "✓ Custom shirt generated"
else
    echo "✗ Failed to generate custom shirt"
    exit 1
fi
echo

# Test 5: Verify parameter-only mode still works
echo "Test 5: Verify parameter-only bespoke mode still works"
python3 interactive_generator.py --pattern shirt --bespoke measurements_shirt_example.json --gender m --style Gilewska --output /tmp/test_output 2>&1 | grep -E "(BESPOKE|Pattern saved)"
if [ -f /tmp/test_output/shirt_M44G.pdf ]; then
    echo "✓ Parameter-only mode works"
else
    echo "✗ Failed parameter-only mode"
    exit 1
fi
echo

echo "=========================================="
echo "All tests passed! ✓"
echo "=========================================="
echo
echo "Generated files:"
ls -lh /tmp/test_output/*.pdf
