#!/usr/bin/env python3
"""
Interactive Pattern Generator

This script provides an interactive interface for generating sewing patterns
with either standard sizes or bespoke measurements from JSON files.

Features:
- Standard size selection (uses OpenPattern's built-in size tables)
- Bespoke measurements from JSON files
- Interactive prompts with sensible defaults
- Command-line argument support for automation
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


# Default configuration
DEFAULTS = {
    'pattern_type': 'bodice',
    'size_mode': 'standard',
    'pname': 'W36G',
    'gender': 'w',
    'style': 'Gilewska',
    'output_dir': 'output',
    'measurements_file': None
}

# Available pattern types and their configurations
PATTERN_TYPES = {
    'bodice': {
        'class': OP.Basic_Bodice,
        'styles': ['Gilewska'],
        'default_params': {
            'ease': 8,
            'hip': False,
            'Back_Front_space': 4
        }
    },
    'skirt': {
        'class': OP.Basic_Skirt,
        'styles': ['Chiappetta'],
        'default_params': {
            'ease': 8,
            'curves': False
        },
        'special_gender': 'G'  # Skirt uses 'G' instead of 'w'/'m'
    },
    'trousers': {
        'class': OP.Basic_Trousers,
        'styles': ['Donnanno'],
        'default_params': {
            'darts': True
        }
    },
    'shirt': {
        'class': OP.Shirt,
        'styles': ['Gilewska'],
        'default_params': {
            'ease': 0,
            'lower_length': 25,
            'hip': False,
            'Back_Front_space': 12,
            'collar_ease': 1,
            'sleeve_lowering': 3,
            'side_ease': 4,
            'shoulder_ease': 1,
            'button_overlap': 2
        }
    },
    'waistcoat': {
        'class': OP.Waist_Coat,
        'styles': ['Gilewska'],
        'default_params': {
            'ease': 8,
            'wc_style': 'Classical',
            'overlap': False
        }
    }
}


def load_measurements_from_json(json_file):
    """
    Load bespoke measurements from a JSON file.
    
    Args:
        json_file: Path to JSON file containing measurements
        
    Returns:
        dict: Measurement parameters
    """
    try:
        with open(json_file, 'r') as f:
            measurements = json.load(f)
        print(f"✓ Loaded measurements from: {json_file}")
        return measurements
    except FileNotFoundError:
        print(f"Error: Measurements file not found: {json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in measurements file: {e}")
        sys.exit(1)


def get_user_input(prompt, default, valid_options=None):
    """
    Get user input with a default value.
    
    Args:
        prompt: Question to ask the user
        default: Default value if user presses Enter
        valid_options: Optional list of valid options
        
    Returns:
        str: User's choice or default
    """
    if valid_options:
        options_str = '/'.join(valid_options)
        full_prompt = f"{prompt} [{options_str}] (default: {default}): "
    else:
        full_prompt = f"{prompt} (default: {default}): "
    
    user_input = input(full_prompt).strip()
    
    if not user_input:
        return default
    
    if valid_options and user_input not in valid_options:
        print(f"Warning: '{user_input}' is not a valid option. Using default: {default}")
        return default
    
    return user_input


def validate_waistcoat_gender(pattern_type, gender):
    """
    Validate and adjust gender for waistcoat patterns.
    
    Args:
        pattern_type: The pattern type being generated
        gender: The requested gender code
        
    Returns:
        str: The validated/adjusted gender code
    """
    if pattern_type == 'waistcoat' and gender == 'w':
        print("\nWarning: Waistcoat patterns only support men's sizes.")
        print("Changing gender to 'm' (men)...")
        return 'm'
    return gender


def generate_pattern_standard(pattern_type, pname, gender, style, output_dir, **extra_params):
    """
    Generate a pattern using standard size.
    
    Args:
        pattern_type: Type of pattern (bodice, skirt, trousers, shirt, waistcoat)
        pname: Pattern name/size code (e.g., W36G, M44D)
        gender: Gender code ('w' for women, 'm' for men, 'G' for skirts)
        style: Drafting style (Gilewska, Chiappetta, Donnanno)
        output_dir: Output directory for PDF
        **extra_params: Additional parameters specific to pattern type
        
    Returns:
        str: Path to generated PDF file
    """
    config = PATTERN_TYPES[pattern_type]
    pattern_class = config['class']
    
    # Validate gender compatibility for specific pattern types
    if pattern_type == 'waistcoat' and gender == 'w':
        print("\n" + "="*60)
        print("ERROR: Women's waistcoat patterns are not supported")
        print("="*60)
        print("The OpenPattern library's Waist_Coat class currently only")
        print("supports men's sizes. Please use a men's size code (e.g., M44G)")
        print("or choose a different pattern type.")
        print("="*60)
        sys.exit(1)
    
    # Use special gender code if required (e.g., skirt uses 'G')
    if 'special_gender' in config:
        gender = config['special_gender']
    
    # Merge default parameters with provided extras
    params = {**config['default_params'], **extra_params}
    
    print(f"\n{'='*60}")
    print(f"Generating {pattern_type.upper()} pattern")
    print(f"{'='*60}")
    print(f"  Pattern name: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate pattern based on type
    if pattern_type == 'trousers':
        # Trousers use a different API
        pattern = pattern_class(
            pname=pname,
            gender=gender,
            style=style,
            darts=params['darts'],
            figPATH=output_dir + "/",
            frmt="pdf",
        )
        pattern.draw_basic_trousers(
            dic={"Pattern": f"Basic {pattern_type}"}, 
            save=True
        )
        pdf_path = os.path.join(output_dir, f'{pname}_basic_{pattern_type}.pdf')
    else:
        # Standard pattern generation
        pattern = pattern_class(
            pname=pname,
            gender=gender,
            style=style,
            **params
        )
        pattern.draw()
        
        # Save as PDF
        pdf_path = os.path.join(output_dir, f'{pattern_type}_{pname}.pdf')
        plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
        plt.close()
    
    print(f"\n✓ Pattern saved: {pdf_path}")
    return pdf_path


def generate_pattern_bespoke(pattern_type, measurements, gender, style, output_dir):
    """
    Generate a pattern using bespoke measurements from JSON.
    
    Args:
        pattern_type: Type of pattern
        measurements: Dictionary of measurements and parameters
        gender: Gender code
        style: Drafting style
        output_dir: Output directory
        
    Returns:
        str: Path to generated PDF
    """
    # Check if this is a full body measurements file (has _metadata or measurements key)
    if '_metadata' in measurements or 'measurements' in measurements:
        return generate_pattern_custom_measurements(
            pattern_type=pattern_type,
            measurements_data=measurements,
            gender=gender,
            style=style,
            output_dir=output_dir
        )
    
    # Extract pname - it's required for parameter-only bespoke measurements
    if 'pname' not in measurements:
        print("Error: JSON measurements file must include a 'pname' field with a valid size code.")
        print("Example: \"pname\": \"W36G\" or \"pname\": \"M44G\"")
        print("Or use a full measurements file with '_metadata' and 'measurements' keys.")
        sys.exit(1)
    
    pname = measurements['pname']
    
    # Remove pname from measurements if present (to avoid duplication)
    params = {k: v for k, v in measurements.items() if k != 'pname'}
    
    print(f"\n{'='*60}")
    print(f"Generating BESPOKE {pattern_type.upper()} pattern")
    print(f"{'='*60}")
    print(f"  Pattern name: {pname}")
    print(f"  Using custom measurements from JSON")
    
    # Generate using standard method but with custom parameters
    return generate_pattern_standard(
        pattern_type=pattern_type,
        pname=pname,
        gender=gender,
        style=style,
        output_dir=output_dir,
        **params
    )


def generate_pattern_custom_measurements(pattern_type, measurements_data, gender, style, output_dir):
    """
    Generate a pattern using complete custom body measurements.
    
    Args:
        pattern_type: Type of pattern
        measurements_data: Dictionary with '_metadata' and 'measurements' keys
        gender: Gender code
        style: Drafting style
        output_dir: Output directory
        
    Returns:
        str: Path to generated PDF
    """
    # Extract metadata and measurements
    metadata = measurements_data.get('_metadata', {})
    body_measurements = measurements_data.get('measurements', {})
    
    if not body_measurements:
        print("Error: No 'measurements' key found in JSON file.")
        print("For custom body measurements, use the format from extract_measurements.py")
        sys.exit(1)
    
    # Get a base size to start with (will be overwritten)
    base_size = metadata.get('source_size', 'W36G' if gender == 'w' else 'M44G')
    
    print(f"\n{'='*60}")
    print(f"Generating CUSTOM {pattern_type.upper()} pattern")
    print(f"{'='*60}")
    print(f"  Using custom body measurements")
    print(f"  Base size: {base_size} (measurements will be replaced)")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    print(f"  Total measurements: {len(body_measurements)}")
    
    # Validate gender for waistcoat
    if pattern_type == 'waistcoat' and gender == 'w':
        print("\n" + "="*60)
        print("ERROR: Women's waistcoat patterns are not supported")
        print("="*60)
        print("The OpenPattern library's Waist_Coat class currently only")
        print("supports men's sizes. Please use gender='m'")
        print("="*60)
        sys.exit(1)
    
    config = PATTERN_TYPES[pattern_type]
    pattern_class = config['class']
    
    # Use special gender code if required (e.g., skirt uses 'G')
    original_gender = gender
    if 'special_gender' in config:
        gender = config['special_gender']
    
    # Get default parameters for this pattern type
    params = config['default_params'].copy()
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate pattern based on type
    if pattern_type == 'trousers':
        # Trousers use a different API
        pattern = pattern_class(
            pname=base_size,
            gender=gender,
            style=style,
            darts=params['darts'],
            figPATH=output_dir + "/",
            frmt="pdf",
        )
        
        # Override measurements with custom values
        pattern.m.update(body_measurements)
        
        # Regenerate pattern with custom measurements
        # Note: For trousers, we need to call the drawing method
        pattern.draw_basic_trousers(
            dic={"Pattern": f"Custom {pattern_type}"}, 
            save=True
        )
        pdf_path = os.path.join(output_dir, f'custom_{pattern_type}_{base_size}.pdf')
    else:
        # Standard pattern generation
        pattern = pattern_class(
            pname=base_size,
            gender=gender,
            style=style,
            **params
        )
        
        # Override measurements with custom values
        print(f"\n  Applying {len(body_measurements)} custom measurements...")
        pattern.m.update(body_measurements)
        
        # Note: The pattern has already been calculated in __init__
        # For a complete solution, we would need to recalculate the pattern
        # with the new measurements. This is a limitation of the OpenPattern library.
        # As a workaround, we draw with the updated measurements.
        
        pattern.draw()
        
        # Save as PDF
        pdf_path = os.path.join(output_dir, f'custom_{pattern_type}_{base_size}.pdf')
        plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
        plt.close()
    
    print(f"\n✓ Pattern saved: {pdf_path}")
    print(f"\nNote: Custom body measurements have been applied.")
    print(f"Some calculated values may still be based on the original size {base_size}.")
    print(f"For best results, choose a base size close to your custom measurements.")
    
    return pdf_path


def interactive_mode():
    """Run the generator in interactive mode with user prompts."""
    print("="*60)
    print("Interactive Pattern Generator")
    print("="*60)
    print()
    
    # Pattern type selection
    pattern_types_str = ', '.join(PATTERN_TYPES.keys())
    print(f"Available pattern types: {pattern_types_str}")
    pattern_type = get_user_input(
        "Select pattern type",
        DEFAULTS['pattern_type'],
        list(PATTERN_TYPES.keys())
    )
    
    # Size mode selection
    size_mode = get_user_input(
        "Size mode",
        DEFAULTS['size_mode'],
        ['standard', 'bespoke']
    )
    
    if size_mode == 'bespoke':
        # Bespoke mode - load from JSON
        measurements_file = get_user_input(
            "Path to measurements JSON file",
            'measurements.json'
        )
        
        measurements = load_measurements_from_json(measurements_file)
        
        # Get gender and style
        gender = get_user_input("Gender", 'w', ['w', 'm'])
        gender = validate_waistcoat_gender(pattern_type, gender)
        
        # Get available styles for this pattern type
        styles = PATTERN_TYPES[pattern_type]['styles']
        style = get_user_input("Style", styles[0], styles)
        
        output_dir = get_user_input("Output directory", DEFAULTS['output_dir'])
        
        # Generate pattern
        pdf_path = generate_pattern_bespoke(
            pattern_type=pattern_type,
            measurements=measurements,
            gender=gender,
            style=style,
            output_dir=output_dir
        )
    else:
        # Standard mode - use size codes
        pname = get_user_input("Pattern size code (e.g., W36G, M44D)", DEFAULTS['pname'])
        
        # Extract gender from pname if possible
        if pname[0].upper() in ['W', 'M']:
            default_gender = pname[0].lower()
        else:
            default_gender = 'w'
        
        gender = get_user_input("Gender", default_gender, ['w', 'm'])
        gender = validate_waistcoat_gender(pattern_type, gender)
        
        # Get available styles for this pattern type
        styles = PATTERN_TYPES[pattern_type]['styles']
        style = get_user_input("Style", styles[0], styles)
        
        output_dir = get_user_input("Output directory", DEFAULTS['output_dir'])
        
        # Generate pattern
        pdf_path = generate_pattern_standard(
            pattern_type=pattern_type,
            pname=pname,
            gender=gender,
            style=style,
            output_dir=output_dir
        )
    
    print()
    print("="*60)
    print("✓ Generation complete!")
    print("="*60)


def main():
    """Main entry point with command-line argument support."""
    parser = argparse.ArgumentParser(
        description='Generate sewing patterns with standard or bespoke measurements',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python interactive_generator.py
  
  # Standard size via command line
  python interactive_generator.py --pattern bodice --pname W36G --gender w --style Gilewska
  
  # Bespoke measurements via command line
  python interactive_generator.py --pattern shirt --bespoke measurements.json --gender m --style Gilewska
        """
    )
    
    parser.add_argument(
        '--pattern',
        choices=list(PATTERN_TYPES.keys()),
        default=None,
        help=f"Pattern type (default: {DEFAULTS['pattern_type']})"
    )
    
    parser.add_argument(
        '--pname',
        default=None,
        help=f"Pattern size code for standard sizes (e.g., W36G, M44D) (default: {DEFAULTS['pname']})"
    )
    
    parser.add_argument(
        '--bespoke',
        metavar='JSON_FILE',
        default=None,
        help='Path to JSON file with bespoke measurements'
    )
    
    parser.add_argument(
        '--gender',
        choices=['w', 'm'],
        default=None,
        help=f"Gender: w=women, m=men (default: {DEFAULTS['gender']})"
    )
    
    parser.add_argument(
        '--style',
        default=None,
        help=f"Drafting style (default: {DEFAULTS['style']})"
    )
    
    parser.add_argument(
        '--output',
        default=DEFAULTS['output_dir'],
        help=f"Output directory (default: {DEFAULTS['output_dir']})"
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode (default if no arguments provided)'
    )
    
    args = parser.parse_args()
    
    # If no arguments provided or --interactive specified, run interactive mode
    if args.interactive or (args.pattern is None and args.pname is None and args.bespoke is None):
        interactive_mode()
        return
    
    # Command-line mode
    pattern_type = args.pattern or DEFAULTS['pattern_type']
    gender = args.gender or DEFAULTS['gender']
    style = args.style or DEFAULTS['style']
    output_dir = args.output
    
    if args.bespoke:
        # Bespoke mode
        measurements = load_measurements_from_json(args.bespoke)
        generate_pattern_bespoke(
            pattern_type=pattern_type,
            measurements=measurements,
            gender=gender,
            style=style,
            output_dir=output_dir
        )
    else:
        # Standard mode
        pname = args.pname or DEFAULTS['pname']
        generate_pattern_standard(
            pattern_type=pattern_type,
            pname=pname,
            gender=gender,
            style=style,
            output_dir=output_dir
        )
    
    print()
    print("="*60)
    print("✓ Generation complete!")
    print("="*60)


if __name__ == "__main__":
    main()
