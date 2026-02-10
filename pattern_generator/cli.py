"""
Command-line interface for the sewing pattern generator.
"""

import argparse
import json
import sys
import os

from .measurements import Measurements, DefaultMeasurements
from .patterns import PatternGenerator
from .export import PatternExporter


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate bespoke sewing patterns from measurements",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a shirt pattern with default men's measurements
  generate-pattern shirt --gender mens --output my_shirt
  
  # Generate a vest with custom measurements from JSON file
  generate-pattern vest --measurements measurements.json
  
  # Generate trousers with tiled A4 PDF
  generate-pattern trousers --gender womens --tiled
  
  # Generate coat without JPG thumbnail
  generate-pattern coat --gender mens --no-jpg
        """
    )
    
    parser.add_argument(
        "garment",
        choices=["shirt", "vest", "trousers", "coat"],
        help="Type of garment to generate"
    )
    
    parser.add_argument(
        "--gender",
        choices=["mens", "womens"],
        default="mens",
        help="Gender for default measurements (default: mens)"
    )
    
    parser.add_argument(
        "--size",
        default="medium",
        help="Size for default measurements (default: medium)"
    )
    
    parser.add_argument(
        "--measurements",
        type=str,
        help="Path to JSON file with custom measurements (overrides --gender and --size)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Output directory (default: output)"
    )
    
    parser.add_argument(
        "--tiled",
        action="store_true",
        help="Generate A4-tiled PDF for printing"
    )
    
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Don't generate full-size PDF"
    )
    
    parser.add_argument(
        "--no-jpg",
        action="store_true",
        help="Don't generate JPG thumbnail"
    )
    
    parser.add_argument(
        "--list-measurements",
        action="store_true",
        help="List all required measurements and exit"
    )
    
    args = parser.parse_args()
    
    # List measurements if requested
    if args.list_measurements:
        print_measurements_help()
        return 0
    
    try:
        # Load measurements
        if args.measurements:
            print(f"Loading measurements from {args.measurements}...")
            with open(args.measurements, 'r') as f:
                measurements_dict = json.load(f)
            measurements = Measurements(measurements_dict)
        else:
            print(f"Using default {args.gender} {args.size} measurements...")
            measurements = DefaultMeasurements.get_default(args.gender, args.size)
        
        # Generate pattern
        print(f"Generating {args.garment} pattern...")
        generator = PatternGenerator(measurements)
        
        if args.garment == "shirt":
            pattern_pieces = generator.generate_shirt()
        elif args.garment == "vest":
            pattern_pieces = generator.generate_vest()
        elif args.garment == "trousers":
            pattern_pieces = generator.generate_trousers()
        elif args.garment == "coat":
            pattern_pieces = generator.generate_coat()
        else:
            print(f"Error: Unknown garment type {args.garment}", file=sys.stderr)
            return 1
        
        # Export pattern
        print(f"Exporting pattern to {args.output}/...")
        exporter = PatternExporter(args.output)
        
        title = f"{args.garment.capitalize()} Pattern"
        output_files = exporter.export_pattern(
            pattern_pieces,
            args.garment,
            title,
            full_pdf=not args.no_pdf,
            tiled_pdf=args.tiled,
            jpg=not args.no_jpg
        )
        
        # Print results
        print("\n✓ Pattern generated successfully!")
        print("\nOutput files:")
        for file_type, path in output_files.items():
            print(f"  - {file_type}: {path}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in measurements file - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def print_measurements_help():
    """Print help about measurements."""
    print("\nRequired Measurements (all in centimeters):\n")
    print("Upper body measurements:")
    print("  - chest/bust: Circumference at fullest part of chest")
    print("  - underbust: (Women only) Circumference under bust")
    print("  - waist: Circumference at natural waistline")
    print("  - hip: Circumference at fullest part of hips")
    print("  - shoulder_width: Distance between shoulder points")
    print("  - across_back: Width across shoulder blades")
    print("  - neck: Circumference of neck")
    print("  - sleeve_length: Shoulder to wrist")
    print("  - arm_length: Shoulder to wrist with bent elbow")
    print("  - bicep: Circumference of upper arm")
    print("  - wrist: Circumference of wrist")
    
    print("\nLower body measurements (for trousers):")
    print("  - inseam: Inside leg from crotch to ankle")
    print("  - outseam: Outside leg from waist to ankle")
    print("  - thigh: Circumference of thigh")
    print("  - knee: Circumference of knee")
    print("  - ankle: Circumference of ankle")
    print("  - rise: Waist to crotch")
    
    print("\nVertical measurements:")
    print("  - height: Total height")
    print("  - nape_to_waist: Back of neck to waistline")
    print("  - waist_to_hip: Waist to fullest part of hip")
    
    print("\nExample JSON format:")
    print(json.dumps({
        "chest": 100.0,
        "waist": 85.0,
        "hip": 100.0,
        "shoulder_width": 46.0,
        "neck": 39.0,
        "sleeve_length": 64.0,
        "nape_to_waist": 48.0
    }, indent=2))
    print()


if __name__ == "__main__":
    sys.exit(main())
