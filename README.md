# Sewing Pattern Generator

A simple Python interface to the OpenPattern library for generating professional sewing patterns. This tool creates standard patterns (Bodice, Skirt, Trousers, Shirt, and Waistcoat) and exports them as PDF files.

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

### Interactive Pattern Generator (Recommended)

The interactive generator provides an easy-to-use interface for creating patterns with either standard sizes or bespoke measurements:

```bash
python interactive_generator.py
```

This will prompt you for:
- Pattern type (bodice, skirt, trousers, shirt, waistcoat)
- Size mode (standard or bespoke)
- Size code (e.g., W36G, M44D) or JSON measurement file
- Gender and style preferences
- Output directory

**All prompts include sensible defaults** - just press Enter to accept them.

#### Command-Line Mode

You can also use command-line arguments for automation:

```bash
# Generate with standard size
python interactive_generator.py --pattern bodice --pname W36G --gender w --style Gilewska

# Generate with bespoke measurements from JSON
python interactive_generator.py --pattern shirt --bespoke measurements_shirt_example.json --gender m

# See all options
python interactive_generator.py --help
```

#### Bespoke Measurements

Create custom patterns using JSON files in two ways:

**Option 1: Adjust Parameters (Simple)**
- Modify pattern parameters like ease, lengths, and fit preferences
- Based on a standard size with custom adjustments

**Option 2: Full Custom Measurements (Advanced)**
- Provide complete body measurements for truly bespoke patterns
- All 35+ body measurements can be customized

**NEW: Interactive English Input Tool**
The easiest way to create custom measurements is with English input:

```bash
# Interactive tool with English measurement names
python create_custom_measurements.py

# Or non-interactive
python create_custom_measurements.py --pname W36G --gender w --output my_size.json

# See measurement reference (English to French mapping)
python create_custom_measurements.py --reference
```

The tool will:
1. Prompt you to select a base pattern size
2. Use measurements from that size as defaults
3. Ask for each measurement using clear English names (e.g., "bust_circumference")
4. Convert to French names automatically for OpenPattern compatibility

**Alternative: Manual JSON Creation**
```bash
# Extract standard measurements as a template
python extract_measurements.py --pname W36G --gender w --output my_size.json

# Edit the measurements in the JSON file (uses French names), then generate
python interactive_generator.py --pattern bodice --bespoke my_size.json --gender w
```

See [MEASUREMENTS.md](MEASUREMENTS.md) for detailed documentation on creating measurement files.

### Generate All Pattern Types

Run the main script to generate all pattern types (Bodice, Skirt, Trousers, Shirt, and Waistcoat):

```bash
python generate_patterns.py
```

This will create PDF files in the `output/` directory:
- `bodice_W36G.pdf` - Women's bodice (Gilewska style)
- `skirt_W6C.pdf` - Women's skirt (Chiappetta style)
- `Donnanno_Basic_Trousers_M44D_FullSize.pdf` - Men's trousers (Donnanno style)
- `shirt_M44G.pdf` - Men's shirt (Gilewska style)
- `waistcoat_M44G.pdf` - Men's waistcoat (Gilewska style)

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

#### Generate a Shirt Pattern
```bash
python examples/shirt_example.py
```

#### Generate a Waistcoat Pattern
```bash
python examples/waistcoat_example.py
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
- **Example**: `OP.Basic_Skirt(pname="W6C", gender='G', style='Chiappetta', ease=8, curves=False)`
- **Note**: Skirt patterns use `gender='G'` (general/women) and simpler pattern names like "W6C" instead of "W36C"

### Basic Trousers
- **Style**: Donnanno
- **Parameters**: pname, gender, style, darts
- **Example**: `OP.Basic_Trousers(pname="M44D", gender='m', style='Donnanno', darts=True)`

### Shirt
- **Style**: Gilewska
- **Parameters**: pname, gender, style
- **Example**: `OP.Shirt(pname="M44G", gender='m', style='Gilewska')`

### Waistcoat
- **Style**: Gilewska
- **Parameters**: pname, gender, style
- **Example**: `OP.Waist_Coat(pname="M44G", gender='m', style='Gilewska')`
- **Note**: Currently only supports men's sizes (OpenPattern limitation)

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
p = OP.Basic_Skirt(pname="W6C", gender='G', style='Chiappetta', ease=10, curves=True)

# Women's trousers
trousers = OP.Basic_Trousers(pname="W38D", gender='w', style='Donnanno', darts=True)

# Men's shirt
shirt = OP.Shirt(pname="M44G", gender='m', style='Gilewska')

# Men's waistcoat (note: only men's sizes are supported)
waistcoat = OP.Waist_Coat(pname="M44G", gender='m', style='Gilewska')
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
- `shirt_example.py` - Shirt pattern
- `waistcoat_example.py` - Waistcoat (vest) pattern

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
