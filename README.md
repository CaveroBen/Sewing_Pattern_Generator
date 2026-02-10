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

## Usage

### Basic Usage

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

The patterns are based on standard pattern drafting techniques with appropriate ease allowances:
- **Shirts**: 10cm ease for comfortable fit
- **Vests**: 8cm ease for closer fit
- **Trousers**: 8cm ease with proper rise allowances
- **Coats**: 15cm ease to fit over other clothing

## Technical Details

- **Coordinate System**: Cartesian coordinates in centimeters
- **PDF Resolution**: 100 DPI (sufficient for pattern printing)
- **A4 Page Size**: 21.0 × 29.7 cm
- **Margins**: 1.0 cm on all sides
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
- Integration with OpenPattern library for more sophisticated patterns
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