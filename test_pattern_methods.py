#!/usr/bin/env python3
"""
Comprehensive test of all pattern generation methods.

This script tests:
1. Simple OpenPattern usage (recommended)
2. Basic PatternGenerator (for when OpenPattern is not installed)
"""

import sys

def test_simple_openpattern():
    """Test simple direct OpenPattern usage."""
    print("\n" + "="*60)
    print("TEST 1: Simple OpenPattern Usage (Recommended)")
    print("="*60)
    
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import OpenPattern as OP
        import tempfile
        import os
        
        # Create pattern with standard size
        p = OP.Basic_Bodice(
            pname="W36G",
            gender='w',
            style='Gilewska'
        )
        
        # Draw it
        p.draw()
        
        # Use cross-platform temporary directory
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, 'test_simple_openpattern.png')
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        plt.close()
        
        print("✓ Simple OpenPattern method works!")
        print("  - Used standard size: W36G")
        print(f"  - Pattern saved to: {output_path}")
        return True
        
    except ImportError as e:
        print(f"✗ OpenPattern not available: {e}")
        print("  Install with: git clone https://github.com/fmetivier/OpenPattern.git && cd OpenPattern && pip install -e .")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_basic_pattern_generator():
    """Test basic PatternGenerator with OpenPattern."""
    print("\n" + "="*60)
    print("TEST 2: Basic PatternGenerator (OpenPattern-based)")
    print("="*60)
    
    try:
        from pattern_generator import PatternGenerator, DefaultMeasurements
        
        # Get default measurements
        measurements = DefaultMeasurements.get_default('womens', 'medium')
        
        # Create generator
        generator = PatternGenerator(measurements)
        
        # Generate shirt pattern
        pattern = generator.generate_shirt()
        
        print("✓ Basic PatternGenerator works!")
        print(f"  - Pattern type: {pattern.get('type')}")
        print(f"  - Garment: {pattern.get('garment')}")
        print(f"  - Pattern name: {pattern.get('pname')}")
        print(f"  - Uses OpenPattern: {pattern.get('type') == 'openpattern'}")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "#"*60)
    print("# Pattern Generation Methods Test Suite")
    print("#"*60)
    
    results = []
    
    # Test simple OpenPattern
    results.append(("Simple OpenPattern", test_simple_openpattern()))
    
    # Test basic generator
    results.append(("Basic PatternGenerator", test_basic_pattern_generator()))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\n" + "="*60)
    print("RECOMMENDATION")
    print("="*60)
    print("For professional patterns: Use PatternGenerator or Simple OpenPattern method")
    print("Both methods now use OpenPattern for professional-grade patterns")
    print("\nSee examples/simple_bodice.py for direct OpenPattern usage.")
    print("="*60 + "\n")
    
    # Return exit code
    all_pass = all(result[1] for result in results)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
