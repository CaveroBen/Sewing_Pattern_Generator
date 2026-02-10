#!/usr/bin/env python3
"""
Example: Generate a Basic Bodice Pattern

This example demonstrates how to generate a basic bodice pattern
using the OpenPattern library with Gilewska style drafting.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless systems

import matplotlib.pyplot as plt
import OpenPattern as OP

# Create a women's bodice pattern using Gilewska method
p = OP.Basic_Bodice(
    pname="W36G",      # Pattern name (W=Women, 36=size, G=Gilewska)
    gender='w',        # 'w' for women, 'm' for men
    style='Gilewska'   # Pattern drafting style
)

# Draw and display the pattern
p.draw()

# Save as PDF
plt.savefig('bodice_pattern.pdf', format='pdf', bbox_inches='tight')
print("Bodice pattern saved as 'bodice_pattern.pdf'")

# Display the pattern
plt.show()
