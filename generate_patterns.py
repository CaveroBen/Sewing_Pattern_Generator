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


def generate_bodice(pname="W36G", gender='w', style='Gilewska', output_dir='output', with_sleeves=False, sleeve_style=None):
    """
    Generate a basic bodice pattern.
    
    Args:
        pname: Pattern name (e.g., W36G = Women's size 36, Gilewska style)
        gender: 'w' for women, 'm' for men
        style: Pattern drafting style (e.g., 'Gilewska')
        output_dir: Directory to save the PDF
        with_sleeves: Whether to add sleeves to the bodice
        sleeve_style: Sleeve style ('Gilewska', 'Donnanno', 'Chiappetta'), defaults to bodice style
    """
    print(f"\nGenerating bodice pattern: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    if with_sleeves:
        print(f"  With sleeves: {sleeve_style or style}")
    
    # Create the bodice pattern
    p = OP.Basic_Bodice(
        pname=pname,
        gender=gender,
        style=style
    )
    
    # Add sleeves if requested
    if with_sleeves:
        add_sleeves_to_bodice(p, gender, sleeve_style or style)
    
    # Draw the pattern
    p.draw()
    
    # Save as PDF
    os.makedirs(output_dir, exist_ok=True)
    sleeve_suffix = '_with_sleeves' if with_sleeves else ''
    pdf_path = os.path.join(output_dir, f'bodice_{pname}{sleeve_suffix}.pdf')
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
    print(f"  Saved: {pdf_path}")
    
    plt.close()
    return pdf_path


def add_sleeves_to_bodice(bodice, gender, sleeve_style='Gilewska'):
    """
    Add sleeves to an existing bodice pattern.
    
    This function transforms a basic bodice by adding sleeves according to
    the specified style. The sleeve is automatically fitted to the armhole
    of the bodice.
    
    Args:
        bodice: OP.Basic_Bodice instance
        gender: 'w' for women, 'm' for men
        sleeve_style: Style of sleeve ('Gilewska', 'Donnanno', 'Chiappetta')
    
    Returns:
        The modified bodice with sleeves added
    
    Note:
        Some sleeve styles may only work with specific bodice styles or genders.
        If a sleeve method is not compatible, it will fall back to Gilewska style.
    """
    print(f"  Adding {sleeve_style} sleeves...")
    
    # Map of sleeve methods for each style and gender
    # Note: Not all combinations are available in OpenPattern
    sleeve_methods = {
        ('Gilewska', 'w'): 'Gilewska_basic_sleeve_w',
        ('Gilewska', 'm'): 'Gilewska_basic_sleeve_m',
        ('Chiappetta', 'm'): 'chiappetta_armhole_sleeve_m',
        ('Chiappetta', 'w'): 'chiappetta_basic_sleeve_m',  # Fallback for women
    }
    
    # Get the appropriate sleeve method
    method_name = sleeve_methods.get((sleeve_style, gender))
    
    if not method_name:
        print(f"  Warning: {sleeve_style} sleeves not available for gender '{gender}', using Gilewska")
        method_name = sleeve_methods.get(('Gilewska', gender))
    
    if hasattr(bodice, method_name):
        try:
            method = getattr(bodice, method_name)
            method()
            print(f"  Sleeves added successfully using {method_name}")
        except Exception as e:
            print(f"  Warning: Failed to add {sleeve_style} sleeves: {e}")
            # Try fallback to Gilewska
            if sleeve_style != 'Gilewska':
                print(f"  Trying Gilewska sleeves as fallback...")
                fallback_method = sleeve_methods.get(('Gilewska', gender))
                if fallback_method and hasattr(bodice, fallback_method):
                    try:
                        method = getattr(bodice, fallback_method)
                        method()
                        print(f"  Sleeves added using fallback: {fallback_method}")
                    except Exception as e2:
                        print(f"  Error: Could not add sleeves: {e2}")
    else:
        print(f"  Warning: Method {method_name} not found on bodice")
    
    return bodice


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
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
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
        
        pattern_type = data.get('type', '')
        if not pattern_type:
            raise ValueError("Missing required field 'type' in JSON file")
        
        pattern_type = pattern_type.lower()
        if pattern_type not in ['bodice', 'skirt', 'trousers']:
            raise ValueError(f"Invalid pattern type: '{pattern_type}'. Must be 'bodice', 'skirt', or 'trousers'")
        
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


def ensure_pattern_suffix(name, pattern_type):
    """
    Ensure the pattern name has the correct suffix based on pattern type.
    
    OpenPattern uses specific suffix conventions to identify pattern styles:
    - 'G' for Gilewska style (typically bodice patterns)
    - 'C' for Chiappetta style (typically skirt patterns)
    - 'D' for Donnanno style (typically trousers patterns)
    
    Args:
        name: Pattern name (e.g., 'W36', 'W8', 'M44')
        pattern_type: Type of pattern ('bodice', 'skirt', or 'trousers')
        
    Returns:
        Pattern name with correct suffix (e.g., 'W36G', 'W8C', 'M44D')
    """
    suffix_map = {
        'bodice': 'G',
        'skirt': 'C',
        'trousers': 'D'
    }
    
    suffix = suffix_map.get(pattern_type)
    if suffix and not name.endswith(suffix):
        return f"{name}{suffix}"
    return name


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
    
    # Check for transformations
    transformations = data.get('transformations', {})
    
    # Generate the appropriate pattern type
    # Note: OpenPattern uses standard sizes, but we can still pass the name
    if pattern_type == 'bodice':
        pname = ensure_pattern_suffix(name, 'bodice')
        
        # Check for sleeve transformation
        with_sleeves = transformations.get('add_sleeves', False)
        sleeve_style = transformations.get('sleeve_style', style)
        
        pdf_path = generate_bodice(
            pname=pname,
            gender=gender,
            style=style,
            output_dir=output_dir,
            with_sleeves=with_sleeves,
            sleeve_style=sleeve_style
        )
    elif pattern_type == 'skirt':
        pname = ensure_pattern_suffix(name, 'skirt')
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
        pname = ensure_pattern_suffix(name, 'trousers')
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
  
  # Generate a bodice with sleeves
  python generate_patterns.py --type bodice --size W36G --add-sleeves
  
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
    
    parser.add_argument(
        '--add-sleeves',
        action='store_true',
        help='Add sleeves to bodice pattern (only for bodice type)'
    )
    
    parser.add_argument(
        '--sleeve-style',
        choices=['Gilewska', 'Donnanno', 'Chiappetta'],
        help='Sleeve style (defaults to bodice style)'
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
            # Provide helpful error message with examples based on pattern type
            size_examples = {
                'bodice': 'W36G, W38G, W40G, M44G',
                'skirt': 'W6C, W8C, W10C',
                'trousers': 'M44D, M46D, W38D'
            }
            examples = size_examples.get(args.type, 'W36G, W6C, M44D')
            print(f"Error: --size is required when --type is specified")
            print(f"Example sizes for {args.type}: {examples}")
            sys.exit(1)
        
        pattern_type = args.type.lower()
        size = args.size
        
        # Extract style from size or use provided style
        if pattern_type == 'bodice':
            style = args.style or 'Gilewska'
            gender = args.gender or 'w'
            
            # Check for sleeve transformation
            with_sleeves = args.add_sleeves
            sleeve_style = args.sleeve_style or style
            
            # Warn if sleeve options used without bodice
            if with_sleeves and pattern_type != 'bodice':
                print("Warning: --add-sleeves only applies to bodice patterns")
                with_sleeves = False
            
            generate_bodice(
                pname=size,
                gender=gender,
                style=style,
                output_dir=output_dir,
                with_sleeves=with_sleeves,
                sleeve_style=sleeve_style
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
