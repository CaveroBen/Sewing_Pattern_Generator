#!/usr/bin/env python3
"""
Simple Bodice Pattern Example

This script demonstrates the simplest way to generate a bodice pattern using OpenPattern.
This is the recommended approach for users who want to use OpenPattern directly
with minimal complexity.

Requirements:
    - OpenPattern library must be installed
    - matplotlib for visualization

Installation:
    pip install matplotlib
    git clone https://github.com/fmetivier/OpenPattern.git
    cd OpenPattern
    pip install -e .

Usage:
    python examples/simple_bodice.py
"""

import matplotlib.pyplot as plt
import OpenPattern as OP

def main():
    """Generate and display a simple bodice pattern."""
    
    print("Generating bodice pattern...")
    print("=" * 50)
    
    # Creation de l'instance
    # Create a women's bodice pattern using Gilewska method
    p = OP.Basic_Bodice(
        pname="W36G",      # Pattern name (W = Women, 36 = size, G = Gilewska)
        gender='w',        # 'w' for women, 'm' for men
        style='Gilewska'   # Pattern drafting style
    )
    
    print("✓ Bodice pattern created")
    print(f"  Pattern name: W36G")
    print(f"  Gender: Women")
    print(f"  Style: Gilewska")
    
    # Appel de la fonction de dessin
    # Draw the pattern
    p.draw()
    
    print("\n✓ Pattern drawn successfully")
    print("\nDisplaying pattern... (close window to exit)")
    
    # Show the pattern
    plt.show()
    
    print("\nDone!")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        if "OpenPattern" in str(e):
            print("ERROR: OpenPattern library is not installed.")
            print("\nTo install OpenPattern:")
            print("  git clone https://github.com/fmetivier/OpenPattern.git")
            print("  cd OpenPattern")
            print("  pip install -e .")
            print("\nAlternatively, use the pattern_generator package:")
            print("  python examples/openpattern_example.py")
        else:
            raise
