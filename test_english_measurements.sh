#!/bin/bash
# Test script for create_custom_measurements.py

set -e

echo "=========================================="
echo "Testing create_custom_measurements.py"
echo "=========================================="
echo

# Test 1: Show reference
echo "Test 1: Display measurement reference"
python3 create_custom_measurements.py --reference > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Reference display works"
else
    echo "✗ Reference display failed"
    exit 1
fi
echo

# Test 2: Create with non-interactive mode
echo "Test 2: Create measurements with non-interactive mode"
echo -e "no\nno\nno\nno\nno\nno\nno" | python3 create_custom_measurements.py \
    --pname W36G --gender w --style Gilewska --output /tmp/test_english_W36G.json > /dev/null 2>&1

if [ -f /tmp/test_english_W36G.json ]; then
    echo "✓ Measurement file created"
    
    # Check if it has the correct structure
    if grep -q '"_metadata"' /tmp/test_english_W36G.json && \
       grep -q '"measurements"' /tmp/test_english_W36G.json && \
       grep -q 'created_with' /tmp/test_english_W36G.json; then
        echo "✓ File has correct structure"
    else
        echo "✗ File structure is incorrect"
        exit 1
    fi
else
    echo "✗ Measurement file not created"
    exit 1
fi
echo

# Test 3: Verify English to French conversion
echo "Test 3: Verify English to French conversion"
if grep -q 'tour_poitrine' /tmp/test_english_W36G.json && \
   grep -q 'tour_taille' /tmp/test_english_W36G.json && \
   grep -q 'longueur_dos' /tmp/test_english_W36G.json; then
    echo "✓ French measurement names present"
else
    echo "✗ French measurement names missing"
    exit 1
fi
echo

# Test 4: Verify file works with interactive_generator
echo "Test 4: Generate pattern with created measurements"
python3 interactive_generator.py --pattern bodice \
    --bespoke /tmp/test_english_W36G.json \
    --gender w --style Gilewska \
    --output /tmp/test_english_output > /dev/null 2>&1

if [ -f /tmp/test_english_output/custom_bodice_W36G.pdf ]; then
    echo "✓ Pattern generated successfully with English-input measurements"
else
    echo "✗ Pattern generation failed"
    exit 1
fi
echo

# Test 5: Create men's size
echo "Test 5: Create measurements for men's size"
echo -e "no\nno\nno\nno\nno\nno\nno" | python3 create_custom_measurements.py \
    --pname M44G --gender m --style Gilewska --output /tmp/test_english_M44G.json > /dev/null 2>&1

if [ -f /tmp/test_english_M44G.json ]; then
    echo "✓ Men's measurement file created"
else
    echo "✗ Men's measurement file not created"
    exit 1
fi
echo

echo "=========================================="
echo "All tests passed! ✓"
echo "=========================================="
echo
echo "Generated files:"
ls -lh /tmp/test_english*.json /tmp/test_english_output/*.pdf 2>/dev/null
