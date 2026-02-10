#!/usr/bin/env python3
"""
Example script demonstrating how to use the PatternGenerator with OpenPattern.

This script shows how the PatternGenerator now uses OpenPattern methods
for professional-grade sewing patterns.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pattern_generator import (
    PatternGenerator, 
    Measurements,
    DefaultMeasurements
)
from pattern_generator.export import PatternExporter

def main():
    print("Sewing Pattern Generator - OpenPattern Example")
    print("=" * 60)
    
    # Load measurements
    print("\n1. Loading measurements...")
    measurements = DefaultMeasurements.get_default("womens", "medium")
    print(f"   ✓ Loaded womens/medium measurements")
    print(f"   - Bust: {measurements.get('bust')} cm")
    print(f"   - Waist: {measurements.get('waist')} cm")
    
    # Create PatternGenerator (now uses OpenPattern internally)
    print("\n2. Creating PatternGenerator...")
    generator = PatternGenerator(measurements)
    print(f"   ✓ PatternGenerator created")
    print(f"   - Uses OpenPattern for professional patterns")
    
    # Generate a shirt pattern
    print("\n3. Generating shirt pattern...")
    pattern = generator.generate_shirt()
    print(f"   ✓ Pattern generated successfully")
    print(f"   - Pattern type: {pattern.get('type')}")
    print(f"   - Garment: {pattern.get('garment')}")
    print(f"   - OpenPattern size: {pattern.get('pname')}")
    
    # Export to PDF
    print("\n4. Exporting pattern to PDF...")
    exporter = PatternExporter("output")
    files = exporter.export_pattern(
        pattern,
        "shirt",
        "Women's Shirt Pattern",
        full_pdf=True,
        tiled_pdf=True,
        jpg=True
    )
    
    print(f"   ✓ Pattern exported successfully")
    for file_type, path in files.items():
        print(f"   - {file_type}: {path}")
    
    print("\n" + "=" * 60)
    print("SUCCESS!")
    print("=" * 60)
    print("\nThe PatternGenerator now uses OpenPattern methods directly")
    print("for professional-grade patterns with proper drafting techniques.")
    print("\nGenerated files can be found in the 'output' directory.")
    print("\nFor direct OpenPattern usage, see: simple_bodice.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
