#!/usr/bin/env python3
"""
OpenPattern Interface - Sewing Pattern Generator

This script generates standard sewing patterns using OpenPattern library:
- Basic Bodice (Gilewska style)
- Basic Skirt (Chiappetta style)  
- Basic Trousers (Donnanno style)

All patterns are exported as PDF files.
"""

import os
import sys
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
        gender: Gender code (use 'G' for general/women)
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
    p = OP.Basic_Skirt(
        pname=pname,
        style=style,
        gender=gender,
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


def main():
    """Main function to generate all pattern types."""
    print("=" * 60)
    print("OpenPattern Interface - Sewing Pattern Generator")
    print("=" * 60)
    
    output_dir = 'output'
    
    # Generate all pattern types
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
