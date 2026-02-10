#!/usr/bin/env python3
"""
Test script for the interactive PDF pattern generator.
Tests different combinations of inputs.
"""

import os
import sys
import subprocess
import tempfile
import shutil

def run_test(test_name, inputs, expected_files):
    """Run a test case with given inputs."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    
    # Create temporary output directory
    test_output = os.path.join(tempfile.gettempdir(), f'pattern_test_{test_name.replace(" ", "_")}')
    if os.path.exists(test_output):
        shutil.rmtree(test_output)
    
    # Prepare inputs (add output directory)
    full_inputs = inputs + [test_output, 'y']
    input_str = '\n'.join(full_inputs) + '\n'
    
    # Run the script
    try:
        result = subprocess.run(
            [sys.executable, 'generate_pdf_pattern.py'],
            input=input_str,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"✗ FAILED: Script returned exit code {result.returncode}")
            print("STDERR:", result.stderr)
            return False
        
        # Check for expected files
        missing_files = []
        for expected_file in expected_files:
            file_path = os.path.join(test_output, expected_file)
            if not os.path.exists(file_path):
                missing_files.append(expected_file)
            else:
                size_kb = os.path.getsize(file_path) / 1024
                print(f"  ✓ {expected_file} ({size_kb:.1f} KB)")
        
        if missing_files:
            print(f"✗ FAILED: Missing files: {', '.join(missing_files)}")
            return False
        
        print(f"✓ PASSED: All expected files generated")
        
        # Cleanup
        shutil.rmtree(test_output)
        return True
        
    except subprocess.TimeoutExpired:
        print(f"✗ FAILED: Script timeout")
        return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def main():
    """Run all test cases."""
    print("="*60)
    print("PDF Pattern Generator Test Suite")
    print("="*60)
    
    tests = [
        {
            'name': 'Women Bodice with A4',
            'inputs': ['womens', '38', 'bodice', 'y', 'y'],
            'files': ['bodice_pattern.pdf', 'bodice_pattern_tiled.pdf', 'bodice_pattern.jpg']
        },
        {
            'name': 'Men Trousers A4 only',
            'inputs': ['mens', '42', 'trousers', 'y', 'n'],
            'files': ['trousers_pattern_tiled.pdf', 'trousers_pattern.jpg']
        },
        {
            'name': 'Women Skirt full PDF',
            'inputs': ['womens', '40', 'skirt', 'n', 'y'],
            'files': ['skirt_pattern.pdf', 'skirt_pattern.jpg']
        },
        {
            'name': 'Default values',
            'inputs': ['', '', '', 'y', 'y'],  # All defaults
            'files': ['bodice_pattern.pdf', 'bodice_pattern_tiled.pdf', 'bodice_pattern.jpg']
        }
    ]
    
    results = []
    for test in tests:
        passed = run_test(test['name'], test['inputs'], test['files'])
        results.append((test['name'], passed))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{passed_count}/{total_count} tests passed")
    print(f"{'='*60}\n")
    
    return 0 if passed_count == total_count else 1


if __name__ == "__main__":
    sys.exit(main())
