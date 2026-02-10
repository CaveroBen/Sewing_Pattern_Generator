# Sewing Pattern Generator

A Python-based tool for generating bespoke sewing patterns based on custom measurements. This tool creates professional sewing patterns for shirts, vests (waistcoats), trousers, and coats with options for PDF output (full-size or A4-tiled) and JPG thumbnails.

## Features

- **Multiple Garment Types**: Generate patterns for shirts, vests, trousers, and coats
- **Custom Measurements**: Input your own measurements or use default sizing
- **Multiple Output Formats**:
  - Full-size PDF for professional printing
  - A4-tiled PDF for home printing
  - JPG thumbnails for preview
- **Default Sizing**: Built-in standard measurements for men's and women's sizes
- **1:1 Scale**: Patterns are generated at full scale for direct printing

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install the Package

```bash
pip install -e .
```

This will install the `generate-pattern` command globally.

### Optional: Install OpenPattern (Recommended)

For formal pattern drafting using established patternmaking methodologies, you can install the OpenPattern library:

```bash
# Clone the OpenPattern repository
git clone https://github.com/fmetivier/OpenPattern.git

# Navigate to the OpenPattern directory
cd OpenPattern

# Install OpenPattern
pip install -e .
```

**What is OpenPattern?**

OpenPattern is a Python library for generating professional sewing patterns based on established patternmaking techniques by Jacqueline Chiappetta, Theresa Gilewska, and Antonio Donnano. It provides:

- More sophisticated pattern blocks with professional-grade accuracy
- Support for standard sizing systems (French, Italian)
- Advanced features like dart manipulation and pattern grading
- Scriptable pattern customization

**Note:** OpenPattern is optional. The basic pattern generator works without it, but OpenPattern provides more professional results for serious sewers and tailors.

## Usage

### Simple OpenPattern Usage (Recommended)

If you have OpenPattern installed, you can use it directly with a simple Python script for professional-grade patterns:

```python
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
plt.show()
```

Run the included example:
```bash
python examples/simple_bodice.py
```

This is the simplest way to generate professional bodice patterns with minimal complexity.

### Command-Line Usage

Alternatively, use the command-line tool for basic patterns:

Generate a pattern with default measurements:

```bash
generate-pattern shirt --gender mens
```

### Custom Measurements

Create a JSON file with your measurements (measurements.json):

```json
{
  "chest": 100.0,
  "waist": 85.0,
  "hip": 100.0,
  "shoulder_width": 46.0,
  "neck": 39.0,
  "sleeve_length": 64.0,
  "bicep": 33.0,
  "wrist": 17.0,
  "nape_to_waist": 48.0
}
```

Generate pattern with custom measurements:

```bash
generate-pattern shirt --measurements measurements.json
```

### Generate Different Garments

```bash
# Shirt
generate-pattern shirt --gender mens

# Vest/Waistcoat
generate-pattern vest --gender womens

# Trousers
generate-pattern trousers --gender mens --tiled

# Coat
generate-pattern coat --gender womens --output my_coat
```

### Output Options

```bash
# Generate A4-tiled PDF for home printing
generate-pattern shirt --tiled

# Specify output directory
generate-pattern vest --output my_patterns

# Skip JPG thumbnail
generate-pattern trousers --no-jpg

# Skip full-size PDF (only generate tiled)
generate-pattern coat --tiled --no-pdf
```

### List Required Measurements

To see all available measurements and their descriptions:

```bash
generate-pattern --list-measurements
```

## Command-Line Options

```
usage: generate-pattern [-h] [--gender {mens,womens}] [--size SIZE]
                       [--measurements MEASUREMENTS] [--output OUTPUT]
                       [--tiled] [--no-pdf] [--no-jpg]
                       [--list-measurements]
                       {shirt,vest,trousers,coat}

Arguments:
  garment              Type of garment: shirt, vest, trousers, or coat

Options:
  --gender             Gender for default measurements (mens/womens)
  --size               Size for default measurements (default: medium)
  --measurements       Path to JSON file with custom measurements
  --output             Output directory (default: output)
  --tiled              Generate A4-tiled PDF for printing
  --no-pdf             Don't generate full-size PDF
  --no-jpg             Don't generate JPG thumbnail
  --list-measurements  List all required measurements
```

## Measurements Guide

All measurements should be in centimeters (cm).

### Upper Body Measurements
- **chest/bust**: Circumference at fullest part of chest
- **waist**: Circumference at natural waistline
- **hip**: Circumference at fullest part of hips
- **shoulder_width**: Distance between shoulder points
- **neck**: Circumference of neck at base
- **sleeve_length**: Shoulder point to wrist
- **bicep**: Circumference of upper arm
- **wrist**: Circumference of wrist

### Lower Body Measurements (for Trousers)
- **inseam**: Inside leg from crotch to ankle
- **outseam**: Outside leg from waist to ankle
- **thigh**: Circumference of thigh
- **knee**: Circumference of knee
- **ankle**: Circumference of ankle
- **rise**: Waist to crotch (front rise)

### Vertical Measurements
- **height**: Total body height
- **nape_to_waist**: Back of neck to waistline
- **waist_to_hip**: Waist to fullest part of hip

## Default Measurements

The tool includes default measurements for:
- Men's Medium (chest 38-40" / 96.5-101.5 cm)
- Women's Medium (UK 12-14 / US 8-10)

## Output Files

The tool generates the following files in the output directory:

1. **Full-size PDF** (`{garment}_pattern.pdf`): 
   - Complete pattern at 1:1 scale
   - Ready for professional printing
   - Includes scale reference and grid

2. **Tiled A4 PDF** (`{garment}_pattern_tiled.pdf`):
   - Pattern split across multiple A4 sheets
   - Perfect for home printing
   - Includes alignment marks and tile numbers

3. **JPG Thumbnail** (`{garment}_pattern.jpg`):
   - Preview image of the pattern
   - Maximum 1200px dimension
   - Useful for quick reference

## Examples

### Example 1: Quick Start with Defaults

```bash
generate-pattern shirt --gender mens
```

This creates:
- `output/shirt_pattern.pdf`
- `output/shirt_pattern.jpg`

### Example 2: Custom Vest with Tiled Output

```bash
generate-pattern vest --measurements my_measurements.json --tiled --output my_vest
```

This creates:
- `my_vest/vest_pattern.pdf`
- `my_vest/vest_pattern_tiled.pdf`
- `my_vest/vest_pattern.jpg`

### Example 3: Women's Trousers

```bash
generate-pattern trousers --gender womens --tiled
```

## Pattern Drafting Method

This package supports two pattern drafting methods:

### 1. Basic Pattern Generator (Default)

The basic patterns are based on standard pattern drafting techniques with appropriate ease allowances:
- **Shirts**: 10cm ease for comfortable fit
- **Vests**: 8cm ease for closer fit
- **Trousers**: 8cm ease with proper rise allowances
- **Coats**: 15cm ease to fit over other clothing

**Pattern Features:**
- **Smooth, realistic curves**: Armholes, necklines, and sleeve caps use cubic spline interpolation for professional appearance
- **Proper layout**: Pattern pieces are automatically arranged side-by-side with appropriate spacing
- **Professional markings**: Includes grainline arrows, pattern piece labels, and cutting instructions
- **Scale reference**: 10cm scale bar and grid for accurate printing
- **Pattern information**: Seam allowance notes and printing instructions included

These patterns use simplified geometric calculations with professional-grade curve generation, suitable for home sewing projects.

### 2. OpenPattern Generator (Optional)

When OpenPattern is installed, you can use the formal pattern drafting method based on professional patternmaking techniques:
- Uses established methodologies by Jacqueline Chiappetta, Theresa Gilewska, and Antonio Donnano
- Provides more accurate pattern blocks with proper dart placement
- Supports advanced features like pattern grading and customization
- Generates patterns compatible with industry standards

To use OpenPattern in your Python scripts:

```python
from pattern_generator import OpenPatternGenerator, Measurements

# Check if OpenPattern is available
if OpenPatternGenerator.is_available():
    measurements = Measurements({"chest": 100, "waist": 85, ...})
    generator = OpenPatternGenerator(measurements)
    pattern = generator.generate_shirt()
else:
    print("OpenPattern not installed, using basic generator")
```

## Technical Details

- **Coordinate System**: Cartesian coordinates in centimeters
- **PDF Resolution**: 100 DPI (sufficient for pattern printing)
- **Curve Generation**: Cubic spline interpolation for smooth, realistic pattern curves
- **Layout Algorithm**: Automatic piece positioning with 5cm spacing between pieces
- **Pattern Markings**: Grainline arrows, labels, cutting instructions, and scale reference
- **A4 Page Size**: 21.0 × 29.7 cm
- **Margins**: 2.0 cm on all sides
- **JPG Quality**: 85% (balanced quality/size)

## Troubleshooting

### Issue: Command not found
```bash
# Make sure the package is installed
pip install -e .

# Or run directly with Python
python -m pattern_generator.cli shirt --gender mens
```

### Issue: Invalid measurements
- Ensure all measurements are in centimeters
- Check that JSON file is properly formatted
- Use `--list-measurements` to see required fields

### Issue: PDF too large for printing
- Use the `--tiled` option to split into A4 sheets
- Adjust measurements to reduce overall size

## Future Enhancements

Potential improvements for future versions:
- ✅ Integration with OpenPattern library for more sophisticated patterns (implemented)
- Command-line option to choose between basic and OpenPattern generators
- Additional garment types (dresses, skirts, jackets)
- More size options (S, L, XL, etc.)
- Pattern grading between sizes
- Seam allowance options
- Interactive web interface
- Pattern customization options (collar styles, sleeve types, etc.)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Pattern drafting principles based on standard tailoring techniques
- Inspired by the OpenPattern project for sewing pattern generation