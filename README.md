# Sewing Pattern Generator

A simple Python interface to the OpenPattern library for generating professional sewing patterns. This tool creates standard patterns (Bodice, Skirt, and Trousers) and exports them as PDF files.

## About OpenPattern

OpenPattern is a Python library for generating professional sewing patterns based on established patternmaking techniques by Jacqueline Chiappetta, Theresa Gilewska, and Antonio Donnanno. It provides:

- Professional-grade pattern blocks with accurate drafting
- Support for standard sizing systems (French, Italian)
- Multiple drafting styles from renowned pattern makers
- High-quality pattern generation suitable for professional use

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Install OpenPattern:
```bash
pip install git+https://github.com/fmetivier/OpenPattern.git
```

## Usage

### Generate All Pattern Types

Run the main script to generate all three pattern types (Bodice, Skirt, and Trousers):

```bash
python generate_patterns.py
```

This will create three PDF files in the `output/` directory:
- `bodice_W36G.pdf` - Women's bodice (Gilewska style)
- `skirt_W36C.pdf` - Women's skirt (Chiappetta style)
- `M44D_basic_trousers.pdf` - Men's trousers (Donnanno style)

### Individual Pattern Examples

You can also run individual pattern examples from the `examples/` directory:

#### Generate a Bodice Pattern
```bash
python examples/bodice_example.py
```

#### Generate a Skirt Pattern
```bash
python examples/skirt_example.py
```

#### Generate a Trousers Pattern
```bash
python examples/trousers_example.py
```

### Use in Your Own Code

You can import and use the pattern generation functions in your own scripts:

```python
import matplotlib.pyplot as plt
import OpenPattern as OP

# Create a women's bodice pattern
p = OP.Basic_Bodice(
    pname="W36G",
    gender='w',
    style='Gilewska'
)

# Draw and save as PDF
p.draw()
plt.savefig('my_bodice.pdf', format='pdf', bbox_inches='tight')
plt.show()
```

## Pattern Types

### Basic Bodice
- **Style**: Gilewska
- **Parameters**: pname, gender, style
- **Example**: `OP.Basic_Bodice(pname="W36G", gender='w', style='Gilewska')`

### Basic Skirt
- **Style**: Chiappetta
- **Parameters**: pname, gender, style, ease, curves
- **Example**: `OP.Basic_Skirt(pname="W36C", gender='w', style='Chiappetta', ease=8, curves=False)`

### Basic Trousers
- **Style**: Donnanno
- **Parameters**: pname, gender, style, darts
- **Example**: `OP.Basic_Trousers(pname="M44D", gender='m', style='Donnanno', darts=True)`

## Pattern Naming Convention

Pattern names follow the OpenPattern convention:
- First letter: Gender ('W' for women, 'M' for men)
- Number: Size (e.g., 36, 38, 40, 44)
- Last letter: Style initial (G=Gilewska, C=Chiappetta, D=Donnanno)

Examples:
- `W36G` - Women's size 36, Gilewska style
- `W40C` - Women's size 40, Chiappetta style
- `M44D` - Men's size 44, Donnanno style

## Customization

You can customize patterns by modifying parameters:

```python
# Women's bodice with different size
p = OP.Basic_Bodice(pname="W40G", gender='w', style='Gilewska')

# Skirt with more ease
p = OP.Basic_Skirt(pname="W38C", gender='w', style='Chiappetta', ease=10, curves=True)

# Women's trousers
pans = OP.Basic_Trousers(pname="W38D", gender='w', style='Donnanno', darts=True)
```

## Output

All patterns are saved as PDF files that can be:
- Viewed on screen
- Printed at full scale for pattern making
- Edited with PDF software if needed

The patterns include professional-grade details like:
- Accurate pattern pieces
- Proper seam allowances
- Grainlines and notches
- Pattern labels

## Examples Directory

The `examples/` directory contains individual scripts for each pattern type:
- `bodice_example.py` - Basic bodice pattern
- `skirt_example.py` - Basic skirt pattern
- `trousers_example.py` - Basic trousers pattern

See the [examples/README.md](examples/README.md) for more details.

## Troubleshooting

### OpenPattern Not Installed
If you get an error about OpenPattern not being installed:
```bash
pip install git+https://github.com/fmetivier/OpenPattern.git
```

### Display Issues
If patterns don't display properly, make sure you have a display configured. On headless systems, use:
```python
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
```

## License

This project is open source and available under the MIT License.

## Acknowledgments

- OpenPattern library by François Métivier
- Pattern drafting methods by Jacqueline Chiappetta, Theresa Gilewska, and Antonio Donnanno
