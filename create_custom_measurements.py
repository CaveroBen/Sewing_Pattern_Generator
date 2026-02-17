#!/usr/bin/env python3
"""
Create Custom Measurements (English Input)

This interactive tool helps users create custom measurement files by:
1. Starting with a standard pattern size as a base
2. Prompting for measurements in English with clear descriptions
3. Using existing measurements as defaults
4. Converting to French names for OpenPattern compatibility
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


# Comprehensive French to English translation dictionary
# Format: french_name: (english_name, description, category)
MEASUREMENT_TRANSLATIONS = {
    # Torso/Circumference measurements
    'tour_poitrine': ('bust_circumference', 'Bust/chest circumference', 'Torso'),
    'tour_taille': ('waist_circumference', 'Waist circumference', 'Torso'),
    'tour_bassin': ('hip_circumference', 'Hip circumference (at fullest part)', 'Torso'),
    'tour_petites_hanches': ('small_hip_circumference', 'Small hip circumference', 'Torso'),
    'tour_encolure': ('neck_circumference', 'Neck circumference', 'Torso'),
    
    # Length measurements
    'longueur_dos': ('back_length', 'Back length (nape to waist)', 'Lengths'),
    'longueur_devant': ('front_length', 'Front length (shoulder to waist)', 'Lengths'),
    'longueur_taille_terre': ('waist_to_floor', 'Total height (waist to floor)', 'Lengths'),
    'longueur_epaule': ('shoulder_length', 'Shoulder length', 'Lengths'),
    'longueur_manche': ('sleeve_length', 'Sleeve length (shoulder to wrist)', 'Lengths'),
    'longueur_col_devant': ('front_neck_length', 'Front neck length', 'Lengths'),
    'longueur_col_dos': ('back_neck_length', 'Back neck length', 'Lengths'),
    'longueur_emmanchure_devant': ('front_armhole_length', 'Front armhole length', 'Lengths'),
    'longueur_emmanchure_dos': ('back_armhole_length', 'Back armhole length', 'Lengths'),
    
    # Width measurements
    'carrure_dos': ('back_width', 'Back width (shoulder blade to shoulder blade)', 'Widths'),
    'carrure_devant': ('front_width', 'Front width (chest width)', 'Widths'),
    'largeur_encolure': ('neckline_width', 'Neckline width', 'Widths'),
    
    # Height/Depth measurements
    'hauteur_emmanchure': ('armhole_depth', 'Armhole depth (shoulder to underarm)', 'Heights/Depths'),
    'hauteur_poitrine': ('bust_height', 'Bust point height (shoulder to bust point)', 'Heights/Depths'),
    'hauteur_bassin': ('hip_height', 'Hip height (waist to hip)', 'Heights/Depths'),
    'hauteur_carrure': ('back_shoulder_height', 'Back shoulder height', 'Heights/Depths'),
    'hauteur_petites_hanches': ('small_hip_height', 'Small hip height', 'Heights/Depths'),
    'hauteur_coude': ('elbow_height', 'Elbow height', 'Heights/Depths'),
    'hauteur_taille_genou': ('waist_to_knee', 'Waist to knee height', 'Heights/Depths'),
    'profondeur_encolure_dos': ('back_neckline_depth', 'Back neckline depth', 'Heights/Depths'),
    'profondeur_encolure_devant': ('front_neckline_depth', 'Front neckline depth', 'Heights/Depths'),
    'profondeur_emmanchure': ('armhole_depth_calc', 'Armhole depth (calculated)', 'Heights/Depths'),
    
    # Arm measurements
    'tour_bras': ('upper_arm_circumference', 'Upper arm circumference', 'Arm'),
    'tour_poignet': ('wrist_circumference', 'Wrist circumference', 'Arm'),
    
    # Leg measurements (for trousers)
    'tour_cuisse': ('thigh_circumference', 'Thigh circumference', 'Leg'),
    'tour_genou': ('knee_circumference', 'Knee circumference', 'Leg'),
    'tour_cheville': ('ankle_circumference', 'Ankle circumference', 'Leg'),
    'fourche': ('crotch_depth', 'Crotch depth/rise', 'Leg'),
    'montant': ('crotch_measurement', 'Crotch measurement', 'Leg'),
    
    # Other measurements
    'ecart_poitrine': ('bust_separation', 'Distance between bust points', 'Other'),
}


def create_english_to_french_map():
    """Create reverse mapping from English names to French names."""
    return {english[0]: french for french, english in MEASUREMENT_TRANSLATIONS.items()}


def get_user_input(prompt, default, measurement_type='str'):
    """
    Get user input with a default value.
    
    Args:
        prompt: Question to ask
        default: Default value
        measurement_type: Type of input ('str', 'float', 'int')
    
    Returns:
        User input or default
    """
    if measurement_type == 'float':
        prompt_text = f"{prompt}\n  [Default: {default:.2f} cm, press Enter to keep]: "
    else:
        prompt_text = f"{prompt}\n  [Default: {default}, press Enter to keep]: "
    
    user_input = input(prompt_text).strip()
    
    if not user_input:
        return default
    
    if measurement_type == 'float':
        try:
            return float(user_input)
        except ValueError:
            print(f"  Invalid input, using default: {default}")
            return default
    
    return user_input


def select_base_size():
    """
    Interactive selection of base pattern size.
    
    Returns:
        tuple: (pname, gender, style)
    """
    print("\n" + "="*70)
    print("SELECT BASE PATTERN SIZE")
    print("="*70)
    print("\nChoose a standard size close to your measurements.")
    print("Its measurements will be used as defaults.")
    print()
    print("Common sizes:")
    print("  Women's: W36G, W38G, W40G, W42G, W44G")
    print("  Men's:   M44G, M46G, M48G, M50G, M52G")
    print()
    
    # Get pattern name
    pname = get_user_input(
        "Enter pattern size code (e.g., W36G, M44G)",
        "W36G"
    )
    
    # Extract gender from pattern name
    if pname[0].upper() == 'W':
        default_gender = 'w'
    elif pname[0].upper() == 'M':
        default_gender = 'm'
    else:
        default_gender = 'w'
    
    gender = get_user_input(
        "Enter gender (w for women, m for men)",
        default_gender
    )
    
    style = get_user_input(
        "Enter style (Gilewska, Chiappetta, or Donnanno)",
        "Gilewska"
    )
    
    return pname, gender, style


def extract_base_measurements(pname, gender, style):
    """
    Extract measurements from a standard size.
    
    Args:
        pname: Pattern size code
        gender: Gender code
        style: Pattern style
    
    Returns:
        dict: Base measurements
    """
    print(f"\nExtracting measurements from {pname}...")
    try:
        pattern = OP.Basic_Bodice(pname=pname, gender=gender, style=style)
        return dict(pattern.m)
    except Exception as e:
        print(f"Warning: Could not extract measurements: {e}")
        print("Continuing without base measurements...")
        return {}


def interactive_measurement_input(base_measurements):
    """
    Interactively collect measurements from user with English names.
    
    Args:
        base_measurements: Dictionary of base measurements (in French)
    
    Returns:
        dict: User's custom measurements (in French)
    """
    print("\n" + "="*70)
    print("ENTER YOUR CUSTOM MEASUREMENTS")
    print("="*70)
    print("\nAll measurements are in centimeters.")
    print("Press Enter to keep the default value from the base size.")
    print("Enter 'skip' to skip categories you don't need to modify.")
    print()
    
    custom_measurements = {}
    
    # Group measurements by category
    categories = {}
    for french, (english, desc, category) in MEASUREMENT_TRANSLATIONS.items():
        if category not in categories:
            categories[category] = []
        categories[category].append((french, english, desc))
    
    # Process each category
    for category, measurements in sorted(categories.items()):
        print(f"\n--- {category} ---")
        
        # Ask if user wants to modify this category
        modify = get_user_input(
            f"Do you want to modify {category} measurements? (yes/no/skip)",
            "yes"
        ).lower()
        
        if modify in ['no', 'skip', 'n', 's']:
            # Use defaults for this category
            for french, english, desc in measurements:
                if french in base_measurements:
                    custom_measurements[french] = base_measurements[french]
            continue
        
        # Prompt for each measurement
        for french, english, desc in measurements:
            default = base_measurements.get(french, 0.0)
            
            value = get_user_input(
                f"{english.replace('_', ' ').title()}: {desc}",
                default,
                'float'
            )
            
            custom_measurements[french] = value
    
    return custom_measurements


def save_measurements_file(pname, gender, style, measurements, output_file):
    """
    Save measurements to JSON file.
    
    Args:
        pname: Pattern size code
        gender: Gender code
        style: Pattern style
        measurements: Dictionary of measurements (in French)
        output_file: Output file path
    """
    data = {
        '_metadata': {
            'source_size': pname,
            'gender': gender,
            'style': style,
            'description': f'Custom body measurements based on {pname}',
            'units': 'centimeters',
            'note': 'Created with English input, converted to French names for OpenPattern',
            'created_with': 'create_custom_measurements.py'
        },
        'measurements': measurements
    }
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Custom measurements saved to: {output_file}")
    print(f"  Contains {len(measurements)} body measurements")
    print(f"\nYou can now use this file with:")
    print(f"  python interactive_generator.py --pattern bodice --bespoke {output_file} --gender {gender}")


def show_measurement_reference():
    """Display the complete measurement reference."""
    print("\n" + "="*70)
    print("MEASUREMENT REFERENCE")
    print("="*70)
    print("\nEnglish Name -> French Name (OpenPattern)")
    print()
    
    # Group by category
    categories = {}
    for french, (english, desc, category) in MEASUREMENT_TRANSLATIONS.items():
        if category not in categories:
            categories[category] = []
        categories[category].append((english, french, desc))
    
    for category, measurements in sorted(categories.items()):
        print(f"\n{category}:")
        for english, french, desc in sorted(measurements):
            print(f"  {english:30} -> {french:30} ({desc})")


def main():
    parser = argparse.ArgumentParser(
        description='Create custom measurement file with English input',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended for first-time users)
  python create_custom_measurements.py
  
  # Show measurement reference
  python create_custom_measurements.py --reference
  
  # Non-interactive with base size
  python create_custom_measurements.py --pname W36G --gender w --output my_size.json

The tool will:
  1. Ask you to select a base pattern size
  2. Extract measurements from that size as defaults
  3. Prompt for each measurement with English names and descriptions
  4. Convert to French names and save as JSON
        """
    )
    
    parser.add_argument(
        '--reference',
        action='store_true',
        help='Show measurement reference (English to French mapping)'
    )
    
    parser.add_argument(
        '--pname',
        help='Pattern size code (e.g., W36G, M44G) - skips interactive selection'
    )
    
    parser.add_argument(
        '--gender',
        choices=['w', 'm'],
        help='Gender: w=women, m=men'
    )
    
    parser.add_argument(
        '--style',
        default='Gilewska',
        help='Pattern style (default: Gilewska)'
    )
    
    parser.add_argument(
        '--output',
        default='my_custom_measurements.json',
        help='Output JSON file (default: my_custom_measurements.json)'
    )
    
    args = parser.parse_args()
    
    # Show reference if requested
    if args.reference:
        show_measurement_reference()
        return
    
    print("="*70)
    print("CUSTOM MEASUREMENTS CREATOR - English Input")
    print("="*70)
    print("\nThis tool helps you create custom measurement files using English names.")
    print("Measurements will be converted to French names for OpenPattern compatibility.")
    
    # Get base size
    if args.pname and args.gender:
        pname = args.pname
        gender = args.gender
        style = args.style
        print(f"\nUsing base size: {pname} ({gender}, {style})")
    else:
        pname, gender, style = select_base_size()
    
    # Extract base measurements
    base_measurements = extract_base_measurements(pname, gender, style)
    
    if not base_measurements:
        print("\nWarning: Could not load base measurements.")
        print("You'll need to enter all measurements manually.")
        proceed = get_user_input("Continue? (yes/no)", "yes")
        if proceed.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return
    
    # Collect custom measurements
    custom_measurements = interactive_measurement_input(base_measurements)
    
    # Save to file
    save_measurements_file(pname, gender, style, custom_measurements, args.output)
    
    print("\n" + "="*70)
    print("✓ Custom measurements file created successfully!")
    print("="*70)


if __name__ == "__main__":
    main()
