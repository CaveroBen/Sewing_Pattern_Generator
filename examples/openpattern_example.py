#!/usr/bin/env python3
"""
Example script demonstrating how to use OpenPatternGenerator.

This script shows how to check for OpenPattern availability and use it
to generate professional-grade sewing patterns.
"""

from pattern_generator import (
    PatternGenerator, 
    OpenPatternGenerator, 
    Measurements,
    DefaultMeasurements
)

def main():
    # Load measurements
    measurements = DefaultMeasurements.get_default("mens", "medium")
    
    print("Sewing Pattern Generator - OpenPattern Example")
    print("=" * 50)
    
    # Check if OpenPattern is available
    if OpenPatternGenerator.is_available():
        print("✓ OpenPattern is installed and available")
        print("\nUsing OpenPattern for formal pattern drafting...")
        
        # Create OpenPattern generator
        generator = OpenPatternGenerator(measurements)
        
        # Generate a shirt pattern
        print("Generating shirt pattern...")
        pattern = generator.generate_shirt()
        
        print(f"✓ Pattern generated successfully")
        print(f"  Pattern type: {pattern.get('type', 'unknown')}")
        print(f"  Garment: {pattern.get('garment', 'unknown')}")
        
        print("\nNote: To export OpenPattern patterns to PDF, use")
        print("OpenPattern's built-in export methods:")
        print("  pattern['bodice'].draw({'Pattern': 'Shirt'}, save=True)")
        print("\nThis will save the pattern as 'Shirt.pdf' in the current directory.")
        print("The PDF will be at 1:1 scale suitable for professional printing.")
        
    else:
        print("✗ OpenPattern is not installed")
        print("\nTo use OpenPattern, install it with:")
        print("  git clone https://github.com/fmetivier/OpenPattern.git")
        print("  cd OpenPattern")
        print("  python setup.py install")
        print("\nFalling back to basic pattern generator...")
        
        # Use basic generator instead
        generator = PatternGenerator(measurements)
        pattern = generator.generate_shirt()
        
        print("✓ Shirt pattern generated using basic method")
        print(f"  Pattern pieces: {list(pattern.keys())}")
        print("\nTo export this pattern, use the CLI:")
        print("  generate-pattern shirt --gender mens")

if __name__ == "__main__":
    main()
