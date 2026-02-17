#!/usr/bin/env python3
"""
Example: Generate a Waistcoat Pattern

This example demonstrates how to generate a waistcoat (vest) pattern
using the OpenPattern library with Gilewska style drafting.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless systems

import matplotlib.pyplot as plt
import OpenPattern as OP

# Create a men's waistcoat pattern using Gilewska method
p = OP.Waist_Coat(
    pname="M44G",      # Pattern name (M=Men, 44=size, G=Gilewska)
    gender='m',        # 'm' for men, 'w' for women
    style='Gilewska'   # Pattern drafting style
)

# Draw and display the pattern
p.draw()

# Save as PDF
plt.savefig('waistcoat_pattern.pdf', format='pdf', bbox_inches='tight')
print("Waistcoat pattern saved as 'waistcoat_pattern.pdf'")

# Display the pattern
plt.show()
