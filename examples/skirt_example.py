#!/usr/bin/env python3
"""
Example: Generate a Basic Skirt Pattern

This example demonstrates how to generate a basic skirt pattern
using the OpenPattern library with Chiappetta style drafting.
"""

import matplotlib.pyplot as plt
import OpenPattern as OP

# Create a skirt pattern using Chiappetta method
p = OP.Basic_Skirt(
    pname="W36C",       # Pattern name (W=Women, 36=size, C=Chiappetta)
    style='Chiappetta', # Pattern drafting style
    gender='w',         # 'w' for women, 'm' for men
    ease=8,             # Ease in cm
    curves=False        # Use straight lines instead of curves
)

# Draw and display the pattern
p.draw()

# Save as PDF
plt.savefig('skirt_pattern.pdf', format='pdf', bbox_inches='tight')
print("Skirt pattern saved as 'skirt_pattern.pdf'")

# Display the pattern
plt.show()
