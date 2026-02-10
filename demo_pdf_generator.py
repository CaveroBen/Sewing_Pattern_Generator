#!/usr/bin/env python3
"""
Demonstration script for the interactive PDF pattern generator.

This script demonstrates the key features of generate_pdf_pattern.py
without requiring user input.
"""

import subprocess
import sys
import os
import shutil


def demo_scenario(name, description, inputs):
    """Run a demonstration scenario."""
    print("\n" + "=" * 70)
    print(f"DEMO: {name}")
    print("=" * 70)
    print(f"Description: {description}")
    print("\nUser inputs:")
    for i, input_val in enumerate(inputs[:-1], 1):  # Skip the 'y' confirmation
        if not input_val:
            input_val = "(press Enter for default)"
        print(f"  {i}. {input_val}")
    print("\nGenerating pattern...")
    print("-" * 70)
    
    input_str = '\n'.join(inputs) + '\n'
    result = subprocess.run(
        [sys.executable, 'generate_pdf_pattern.py'],
        input=input_str,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode == 0:
        # Extract just the summary from output
        lines = result.stdout.split('\n')
        in_summary = False
        for line in lines:
            if "Pattern Generation Summary" in line:
                in_summary = True
            if in_summary:
                print(line)
            if in_summary and "✓ Pattern generated successfully!" in line:
                break
        print("✓ Demo completed successfully!\n")
    else:
        print(f"✗ Demo failed: {result.stderr}")


def main():
    """Run all demonstration scenarios."""
    print("\n" + "#" * 70)
    print("# Interactive PDF Pattern Generator - Feature Demonstration")
    print("#" * 70)
    print("\nThis script demonstrates the key features of generate_pdf_pattern.py")
    print("without requiring manual user input.\n")
    
    # Clean up any previous demo output
    demo_dir = "demo_output"
    if os.path.exists(demo_dir):
        shutil.rmtree(demo_dir)
    
    scenarios = [
        {
            "name": "Quick Start - All Defaults",
            "description": "Accept all default values by pressing Enter",
            "inputs": ['', '', '', 'y', 'y', demo_dir, 'y']
        },
        {
            "name": "Women's Bodice with A4 Segmentation",
            "description": "Generate a women's size 40 bodice with A4-tiled PDF for home printing",
            "inputs": ['womens', '40', 'bodice', 'y', 'y', demo_dir, 'y']
        },
        {
            "name": "Men's Trousers - A4 Only",
            "description": "Generate men's size 42 trousers with only A4-tiled PDF (no full-size)",
            "inputs": ['mens', '42', 'trousers', 'y', 'n', demo_dir, 'y']
        },
        {
            "name": "Women's Skirt - Full-Size Only",
            "description": "Generate women's size 36 skirt with only full-size PDF (no A4 tiles)",
            "inputs": ['womens', '36', 'skirt', 'n', 'y', demo_dir, 'y']
        }
    ]
    
    for scenario in scenarios:
        demo_scenario(scenario["name"], scenario["description"], scenario["inputs"])
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print(f"\nAll generated patterns are saved in: {demo_dir}/")
    print("\nKey Features Demonstrated:")
    print("  ✓ Default value handling (press Enter)")
    print("  ✓ Gender selection (mens/womens)")
    print("  ✓ Size selection (34-50)")
    print("  ✓ Style selection (bodice/skirt/trousers)")
    print("  ✓ A4 segmentation option")
    print("  ✓ Full-size PDF option")
    print("  ✓ Custom output directory")
    print("\nTo try it yourself, run:")
    print("  python generate_pdf_pattern.py")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    sys.exit(main())
