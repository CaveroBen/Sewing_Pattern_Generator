#!/usr/bin/env python3
"""
OpenPattern Interface - Sewing Pattern Generator

This script generates standard sewing patterns using OpenPattern library:
- Basic Bodice (Gilewska style)
- Basic Skirt (Chiappetta style)  
- Basic Trousers (Donnanno style)

All patterns are exported as PDF files.

Usage:
    # Generate all patterns
    python generate_patterns.py
    
    # Generate specific pattern type and size
    python generate_patterns.py --type bodice --size W36G
    
    # Generate pattern from bespoke measurements JSON file
    python generate_patterns.py --json test_measurements.json
"""

import os
import sys
import json
import argparse
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless systems
import matplotlib.pyplot as plt

try:
    import OpenPattern as OP
except ImportError:
    print("Error: OpenPattern is not installed.")
    print("Please install it using:")
    print("  pip install git+https://github.com/fmetivier/OpenPattern.git")
    sys.exit(1)


def generate_bodice(pname="W36G", gender='w', style='Gilewska', output_dir='output'):
    """
    Generate a basic bodice pattern.
    
    Args:
        pname: Pattern name (e.g., W36G = Women's size 36, Gilewska style)
        gender: 'w' for women, 'm' for men
        style: Pattern drafting style (e.g., 'Gilewska')
        output_dir: Directory to save the PDF
    """
    print(f"\nGenerating bodice pattern: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    
    # Create the bodice pattern
    p = OP.Basic_Bodice(
        pname=pname,
        gender=gender,
        style=style
    )
    
    # Draw the pattern
    p.draw()
    
    # Save as PDF
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f'bodice_{pname}.pdf')
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
    print(f"  Saved: {pdf_path}")
    
    plt.close()
    return pdf_path


def generate_skirt(pname="W6C", gender='G', style='Chiappetta', ease=8, curves=False, output_dir='output'):
    """
    Generate a basic skirt pattern.
    
    Args:
        pname: Pattern name (e.g., W6C = Women's size, Chiappetta style)
        gender: Gender code - Note: OpenPattern's Basic_Skirt requires 'G' (not 'w' or 'm')
               This is an OpenPattern API requirement, not a standard gender code
        style: Pattern drafting style (e.g., 'Chiappetta')
        ease: Ease in cm
        curves: Whether to use curves
        output_dir: Directory to save the PDF
    """
    print(f"\nGenerating skirt pattern: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    print(f"  Ease: {ease} cm")
    
    # Create the skirt pattern
    # Note: OpenPattern's Basic_Skirt uses different parameters than Basic_Bodice/Basic_Trousers
    p = OP.Basic_Skirt(
        pname=pname,
        style=style,
        gender=gender,  # OpenPattern requires 'G' for skirts
        ease=ease,
        curves=curves
    )
    
    # Draw the pattern
    p.draw()
    
    # Save as PDF
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f'skirt_{pname}.pdf')
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
    print(f"  Saved: {pdf_path}")
    
    plt.close()
    return pdf_path


def generate_trousers(pname="M44D", gender='m', style='Donnanno', darts=True, output_dir='output'):
    """
    Generate a basic trousers pattern.
    
    Args:
        pname: Pattern name (e.g., M44D = Men's size 44, Donnanno style)
        gender: 'w' for women, 'm' for men
        style: Pattern drafting style (e.g., 'Donnanno')
        darts: Whether to include darts
        output_dir: Directory to save the PDF
    """
    print(f"\nGenerating trousers pattern: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    print(f"  Darts: {darts}")
    
    # Create the trousers pattern
    trousers = OP.Basic_Trousers(
        pname=pname,
        gender=gender,
        style=style,
        darts=darts,
        figPATH=output_dir + "/",
        frmt="pdf",
    )
    
    # Draw the pattern
    trousers.draw_basic_trousers(
        dic={"Pattern": "Basic trousers with dart"}, 
        save=True
    )
    
    pdf_path = os.path.join(output_dir, f'{pname}_basic_trousers.pdf')
    print(f"  Saved: {pdf_path}")
    
    plt.close()
    return pdf_path


def load_measurements_from_json(json_file):
    """
    Load bespoke measurements from a JSON file.
    
    Args:
        json_file: Path to JSON file containing measurements
        
    Returns:
        Dictionary with pattern parameters
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        pattern_type = data.get('type', '').lower()
        if pattern_type not in ['bodice', 'skirt', 'trousers']:
            raise ValueError(f"Invalid pattern type: {pattern_type}. Must be 'bodice', 'skirt', or 'trousers'")
        
        return data
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{json_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)


def generate_from_json(json_file, output_dir='output'):
    """
    Generate a pattern from bespoke measurements in a JSON file.
    
    Args:
        json_file: Path to JSON file containing measurements and parameters
        output_dir: Directory to save the PDF
    """
    print(f"\nLoading measurements from: {json_file}")
    data = load_measurements_from_json(json_file)
    
    pattern_type = data['type'].lower()
    name = data.get('name', 'custom')
    style = data.get('style', 'Gilewska')
    gender = data.get('gender', 'w')
    
    print(f"Pattern type: {pattern_type}")
    print(f"Pattern name: {name}")
    
    # Generate the appropriate pattern type
    # Note: OpenPattern uses standard sizes, but we can still pass the name
    if pattern_type == 'bodice':
        pname = f"{name}G" if not name.endswith('G') else name
        pdf_path = generate_bodice(
            pname=pname,
            gender=gender,
            style=style,
            output_dir=output_dir
        )
    elif pattern_type == 'skirt':
        pname = f"{name}C" if not name.endswith('C') else name
        ease = data.get('ease', 8)
        curves = data.get('curves', False)
        pdf_path = generate_skirt(
            pname=pname,
            gender=gender,
            style=style,
            ease=ease,
            curves=curves,
            output_dir=output_dir
        )
    elif pattern_type == 'trousers':
        pname = f"{name}D" if not name.endswith('D') else name
        darts = data.get('darts', True)
        pdf_path = generate_trousers(
            pname=pname,
            gender=gender,
            style=style,
            darts=darts,
            output_dir=output_dir
        )
    
    return pdf_path


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate sewing patterns using OpenPattern library',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all default patterns
  python generate_patterns.py
  
  # Generate a specific bodice pattern
  python generate_patterns.py --type bodice --size W36G
  
  # Generate a skirt pattern
  python generate_patterns.py --type skirt --size W6C
  
  # Generate from custom measurements JSON
  python generate_patterns.py --json test_measurements.json
        """
    )
    
    parser.add_argument(
        '--type',
        choices=['bodice', 'skirt', 'trousers'],
        help='Pattern type to generate'
    )
    
    parser.add_argument(
        '--size',
        help='Pattern size (e.g., W36G for bodice, W6C for skirt, M44D for trousers)'
    )
    
    parser.add_argument(
        '--json',
        help='Path to JSON file with bespoke measurements'
    )
    
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory for PDF files (default: output)'
    )
    
    parser.add_argument(
        '--style',
        help='Pattern drafting style (e.g., Gilewska, Chiappetta, Donnanno)'
    )
    
    parser.add_argument(
        '--gender',
        choices=['w', 'm', 'G'],
        help='Gender code: w=women, m=men, G=general (for skirts)'
    )
    
    return parser.parse_args()


def main():
    """Main function to generate patterns based on arguments."""
    args = parse_arguments()
    
    print("=" * 60)
    print("OpenPattern Interface - Sewing Pattern Generator")
    print("=" * 60)
    
    output_dir = args.output
    
    # Generate from JSON file if provided
    if args.json:
        generate_from_json(args.json, output_dir)
        print("\n" + "=" * 60)
        print("Pattern generation complete!")
        print(f"Pattern saved to '{output_dir}/' directory")
        print("=" * 60)
        return
    
    # Generate specific pattern type if specified
    if args.type:
        if not args.size:
            print("Error: --size is required when --type is specified")
            sys.exit(1)
        
        pattern_type = args.type.lower()
        size = args.size
        
        # Extract style from size or use provided style
        if pattern_type == 'bodice':
            style = args.style or 'Gilewska'
            gender = args.gender or 'w'
            generate_bodice(
                pname=size,
                gender=gender,
                style=style,
                output_dir=output_dir
            )
        elif pattern_type == 'skirt':
            style = args.style or 'Chiappetta'
            gender = args.gender or 'G'
            generate_skirt(
                pname=size,
                gender=gender,
                style=style,
                ease=8,
                curves=False,
                output_dir=output_dir
            )
        elif pattern_type == 'trousers':
            style = args.style or 'Donnanno'
            gender = args.gender or 'm'
            generate_trousers(
                pname=size,
                gender=gender,
                style=style,
                darts=True,
                output_dir=output_dir
            )
        
        print("\n" + "=" * 60)
        print("Pattern generation complete!")
        print(f"Pattern saved to '{output_dir}/' directory")
        print("=" * 60)
        return
    
    # Default: Generate all pattern types
    bodice_pdf = generate_bodice(
        pname="W36G",
        gender='w',
        style='Gilewska',
        output_dir=output_dir
    )
    
    skirt_pdf = generate_skirt(
        pname="W6C",
        gender='G',
        style='Chiappetta',
        ease=8,
        curves=False,
        output_dir=output_dir
    )
    
    trousers_pdf = generate_trousers(
        pname="M44D",
        gender='m',
        style='Donnanno',
        darts=True,
        output_dir=output_dir
    )
    
    print("\n" + "=" * 60)
    print("Pattern generation complete!")
    print(f"All patterns saved to '{output_dir}/' directory")
    print("=" * 60)


if __name__ == "__main__":
    main()
