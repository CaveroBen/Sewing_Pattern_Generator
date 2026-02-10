#!/usr/bin/env python3
"""
Interactive PDF Pattern Generator

This script allows users to generate PDF sewing patterns with interactive prompts.
Users can select size, style (bodice, skirt, trousers), and PDF segmentation options.
"""

import sys
import os

# Add package to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pattern_generator import PatternGenerator, DefaultMeasurements
from pattern_generator.export import PatternExporter


def get_user_input(prompt, default, valid_options=None):
    """
    Get user input with a default value.
    
    Args:
        prompt: The prompt message to display
        default: Default value if user presses Enter
        valid_options: List of valid options (None for any input)
    
    Returns:
        User input or default value
    """
    default_str = f" [{default}]" if default else ""
    if valid_options:
        options_str = "/".join(valid_options)
        full_prompt = f"{prompt} ({options_str}){default_str}: "
    else:
        full_prompt = f"{prompt}{default_str}: "
    
    while True:
        user_input = input(full_prompt).strip()
        
        # Use default if user just pressed Enter
        if not user_input and default:
            return default
        
        # Validate if options are provided
        if valid_options and user_input.lower() not in [opt.lower() for opt in valid_options]:
            print(f"Invalid option. Please choose from: {', '.join(valid_options)}")
            continue
        
        if user_input:
            return user_input.lower() if valid_options else user_input
        
        if not default:
            print("This field is required.")
            continue


def get_yes_no(prompt, default='n'):
    """
    Get yes/no input from user.
    
    Args:
        prompt: The prompt message
        default: Default value ('y' or 'n')
    
    Returns:
        True for yes, False for no
    """
    default_str = 'Y/n' if default == 'y' else 'y/N'
    response = input(f"{prompt} ({default_str}): ").strip().lower()
    
    if not response:
        return default == 'y'
    
    return response in ('y', 'yes')


def get_size_input(gender):
    """
    Get size input from user with gender-appropriate defaults.
    
    Args:
        gender: 'mens' or 'womens'
    
    Returns:
        Size string
    """
    if gender == 'womens':
        print("\nCommon women's sizes: 34, 36, 38, 40, 42, 44, 46")
        default = "38"
    else:
        print("\nCommon men's sizes: 36, 38, 40, 42, 44, 46, 48, 50")
        default = "40"
    
    return get_user_input("Enter size", default)


def generate_bodice_pattern(measurements):
    """Generate bodice pattern (shirt)."""
    generator = PatternGenerator(measurements)
    return generator.generate_shirt()


def generate_skirt_pattern(measurements):
    """Generate skirt pattern (using vest as base)."""
    generator = PatternGenerator(measurements)
    # For now, use vest pattern as a simplified skirt base
    return generator.generate_vest()


def generate_trousers_pattern(measurements):
    """Generate trousers pattern."""
    generator = PatternGenerator(measurements)
    return generator.generate_trousers()


def main():
    """Main interactive pattern generator."""
    print("=" * 60)
    print("Interactive PDF Pattern Generator")
    print("=" * 60)
    print("\nThis tool will help you generate a PDF sewing pattern.")
    print("Press Enter to accept default values shown in [brackets].\n")
    
    # Step 1: Select gender
    print("Step 1: Gender Selection")
    gender = get_user_input("Select gender", "womens", ["mens", "womens"])
    
    # Step 2: Select size
    print("\nStep 2: Size Selection")
    size_input = get_size_input(gender)
    
    # Step 3: Select style
    print("\nStep 3: Style Selection")
    print("Available styles:")
    print("  - bodice: Upper body pattern (shirt/blouse)")
    print("  - skirt: Lower body pattern (skirt/shorts base)")
    print("  - trousers: Full leg pattern (pants/trousers)")
    style = get_user_input("Select style", "bodice", ["bodice", "skirt", "trousers"])
    
    # Step 4: PDF options
    print("\nStep 4: PDF Output Options")
    segment_a4 = get_yes_no("Segment PDF for A4 printing?", 'y')
    full_pdf = get_yes_no("Generate full-size PDF?", 'y')
    
    # Step 5: Output directory
    print("\nStep 5: Output Location")
    output_dir = get_user_input("Output directory", "output")
    
    # Summary
    print("\n" + "=" * 60)
    print("Pattern Generation Summary")
    print("=" * 60)
    print(f"Gender:           {gender}")
    print(f"Size:             {size_input}")
    print(f"Style:            {style}")
    print(f"A4 Segmented:     {'Yes' if segment_a4 else 'No'}")
    print(f"Full-size PDF:    {'Yes' if full_pdf else 'No'}")
    print(f"Output directory: {output_dir}")
    print("=" * 60)
    
    # Confirm
    if not get_yes_no("\nProceed with pattern generation?", 'y'):
        print("Pattern generation cancelled.")
        return 0
    
    try:
        # Load measurements based on gender and size
        print(f"\nLoading {gender} size {size_input} measurements...")
        measurements = DefaultMeasurements.get_default(gender, "medium")
        
        # Generate pattern
        print(f"Generating {style} pattern...")
        if style == "bodice":
            pattern_pieces = generate_bodice_pattern(measurements)
            garment_name = "bodice"
        elif style == "skirt":
            pattern_pieces = generate_skirt_pattern(measurements)
            garment_name = "skirt"
        elif style == "trousers":
            pattern_pieces = generate_trousers_pattern(measurements)
            garment_name = "trousers"
        else:
            print(f"Error: Unknown style '{style}'")
            return 1
        
        # Export pattern
        print(f"Exporting pattern to {output_dir}/...")
        exporter = PatternExporter(output_dir)
        
        title = f"{style.capitalize()} Pattern - Size {size_input}"
        output_files = exporter.export_pattern(
            pattern_pieces,
            garment_name,
            title,
            full_pdf=full_pdf,
            tiled_pdf=segment_a4,
            jpg=True
        )
        
        # Print results
        print("\n" + "=" * 60)
        print("✓ Pattern generated successfully!")
        print("=" * 60)
        print("\nGenerated files:")
        for file_type, path in output_files.items():
            file_size = os.path.getsize(path) / 1024  # KB
            print(f"  ✓ {file_type:12s}: {path} ({file_size:.1f} KB)")
        
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        if full_pdf:
            print("1. Print the full-size PDF at 100% scale (no scaling)")
        if segment_a4:
            print("2. Print the A4-tiled PDF and tape sheets together")
        print("3. Add 1.5cm seam allowance when cutting fabric")
        print("4. Check the 10cm scale bar on the pattern to verify printing accuracy")
        print("=" * 60 + "\n")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error generating pattern: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
