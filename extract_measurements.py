#!/usr/bin/env python3
"""
Standard Measurements Extractor

This utility extracts the complete body measurements from OpenPattern's
standard size tables and saves them as JSON templates. These templates
can be used to create truly bespoke patterns with custom body measurements.
"""

import json
import sys
import argparse

try:
    import OpenPattern as OP
except ImportError:
    print("Error: OpenPattern is not installed.")
    print("Please install it using:")
    print("  pip install git+https://github.com/fmetivier/OpenPattern.git")
    sys.exit(1)


def extract_measurements(pname, gender, style):
    """
    Extract all body measurements from a standard size.
    
    Args:
        pname: Pattern size code (e.g., W36G, M44G)
        gender: Gender code ('w' for women, 'm' for men)
        style: Pattern style (e.g., 'Gilewska')
        
    Returns:
        dict: Complete body measurements
    """
    print(f"Extracting measurements for {pname} ({gender}, {style})...")
    
    # Create a basic bodice pattern to extract measurements
    # (all patterns share the same measurement table)
    pattern = OP.Basic_Bodice(pname=pname, gender=gender, style=style)
    
    # Get all measurements from the pattern
    measurements = dict(pattern.m)
    
    # Add metadata
    result = {
        '_metadata': {
            'source_size': pname,
            'gender': gender,
            'style': style,
            'description': f'Standard body measurements for {pname}',
            'units': 'centimeters',
            'note': 'Modify these values to create custom-fitted patterns'
        },
        'measurements': measurements
    }
    
    return result


def save_measurement_template(output_file, pname='W36G', gender='w', style='Gilewska'):
    """
    Save a measurement template to a JSON file.
    
    Args:
        output_file: Path to output JSON file
        pname: Pattern size code
        gender: Gender code
        style: Pattern style
    """
    data = extract_measurements(pname, gender, style)
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Measurement template saved to: {output_file}")
    print(f"  Contains {len(data['measurements'])} body measurements")
    

def list_available_sizes():
    """List commonly available sizes."""
    print("\nCommon available sizes:")
    print("\nWomen's sizes:")
    print("  W36G, W38G, W40G, W42G, W44G (Gilewska style)")
    print("  W6C, W8C, W10C (Chiappetta style for skirts)")
    print("\nMen's sizes:")
    print("  M44G, M46G, M48G, M50G, M52G (Gilewska style)")
    print("  M44D (Donnanno style)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Extract standard measurements from OpenPattern size tables',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract women's size 36 measurements
  python extract_measurements.py --pname W36G --gender w --output measurements_W36G.json
  
  # Extract men's size 44 measurements
  python extract_measurements.py --pname M44G --gender m --output measurements_M44G.json
  
  # List available sizes
  python extract_measurements.py --list
        """
    )
    
    parser.add_argument(
        '--pname',
        default='W36G',
        help='Pattern size code (default: W36G)'
    )
    
    parser.add_argument(
        '--gender',
        choices=['w', 'm'],
        default='w',
        help='Gender: w=women, m=men (default: w)'
    )
    
    parser.add_argument(
        '--style',
        default='Gilewska',
        help='Pattern style (default: Gilewska)'
    )
    
    parser.add_argument(
        '--output',
        default='standard_measurements.json',
        help='Output JSON file (default: standard_measurements.json)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List available sizes and exit'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_available_sizes()
        return
    
    try:
        save_measurement_template(args.output, args.pname, args.gender, args.style)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
