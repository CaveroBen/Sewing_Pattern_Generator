#!/usr/bin/env python3
"""
Example: Generate a Shirt Pattern

This example demonstrates how to generate a shirt pattern
using the OpenPattern library with Gilewska style drafting.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless systems

import matplotlib.pyplot as plt
import OpenPattern as OP

# Create a men's shirt pattern using Gilewska method
p = OP.Shirt(
    pname="M44G",      # Pattern name (M=Men, 44=size, G=Gilewska)
    gender='m',        # 'm' for men, 'w' for women
    style='Gilewska'   # Pattern drafting style
)

# Draw and display the pattern
p.draw()

# Save as PDF
plt.savefig('shirt_pattern.pdf', format='pdf', bbox_inches='tight')
print("Shirt pattern saved as 'shirt_pattern.pdf'")

# Display the pattern
plt.show()
