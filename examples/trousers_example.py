#!/usr/bin/env python3
"""
Example: Generate Basic Trousers Pattern

This example demonstrates how to generate a basic trousers pattern
using the OpenPattern library with Donnanno style drafting.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless systems

import matplotlib.pyplot as plt
import OpenPattern as OP

# Create a men's trousers pattern using Donnanno method
trousers = OP.Basic_Trousers(
    pname="M44D",       # Pattern name (M=Men, 44=size, D=Donnanno)
    gender="m",         # 'm' for men, 'w' for women
    style="Donnanno",   # Pattern drafting style
    darts=True,         # Include darts in the pattern
    figPATH="./",       # Output directory
    frmt="pdf",         # Output format
)

# Draw the trousers pattern with custom dictionary
trousers.draw_basic_trousers(
    dic={"Pattern": "Basic trousers with dart"}, 
    save=True
)

print("Trousers pattern saved as 'M44D_basic_trousers.pdf'")

# Display the pattern
plt.show()
