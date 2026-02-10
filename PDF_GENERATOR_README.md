# Interactive PDF Pattern Generator

## Overview

`generate_pdf_pattern.py` is an interactive command-line tool that generates PDF sewing patterns with user-friendly prompts. Users can select size, style, and PDF output options through a simple question-and-answer interface.

## Features

- **Interactive Interface**: User-friendly prompts with default values
- **Multiple Styles**: Generate bodice, skirt, or trousers patterns
- **Size Selection**: Support for standard men's and women's sizes
- **PDF Options**: 
  - Full-size PDF for professional printing
  - A4-segmented PDF for home printing
  - JPG thumbnail for preview
- **Default Values**: Press Enter to accept sensible defaults

## Usage

Run the interactive script:

```bash
python generate_pdf_pattern.py
```

The script will guide you through the following steps:

### Step 1: Gender Selection
```
Select gender (mens/womens) [womens]:
```
Press Enter for default (womens) or type `mens`.

### Step 2: Size Selection
```
Common women's sizes: 34, 36, 38, 40, 42, 44, 46
Enter size [38]:
```
Press Enter for default size or enter your size.

### Step 3: Style Selection
```
Select style (bodice/skirt/trousers) [bodice]:
```
Choose from:
- **bodice**: Upper body pattern (shirt/blouse)
- **skirt**: Lower body pattern (skirt/shorts base)
- **trousers**: Full leg pattern (pants/trousers)

### Step 4: PDF Output Options
```
Segment PDF for A4 printing? (Y/n):
Generate full-size PDF? (Y/n):
```
- A4 segmentation splits the pattern across multiple A4 pages for easy home printing
- Full-size PDF is for professional printing at 1:1 scale

### Step 5: Output Location
```
Output directory [output]:
```
Specify where to save the generated files.

## Examples

### Example 1: Quick Start (All Defaults)
Just press Enter for all prompts to generate a women's size 38 bodice pattern with both PDF types.

### Example 2: Men's Trousers with A4 Only
```
Select gender: mens
Enter size: 42
Select style: trousers
Segment PDF for A4 printing? y
Generate full-size PDF? n
Output directory: my_patterns
```

### Example 3: Women's Skirt Full-Size Only
```
Select gender: womens
Enter size: 40
Select style: skirt
Segment PDF for A4 printing? n
Generate full-size PDF? y
Output directory: output
```

## Output Files

The script generates the following files:

1. **Full-size PDF** (`{style}_pattern.pdf`):
   - Professional 1:1 scale pattern
   - Includes scale reference bar
   - Ready for print shop printing

2. **A4-tiled PDF** (`{style}_pattern_tiled.pdf`):
   - Pattern split across multiple A4 pages
   - Includes alignment marks
   - Perfect for home printing
   - Page numbers and tile positions

3. **JPG thumbnail** (`{style}_pattern.jpg`):
   - Preview image of the pattern
   - Quick reference

## Testing

Run the test suite to verify functionality:

```bash
python test_pdf_generator.py
```

The test suite validates:
- Women's bodice patterns
- Men's trousers patterns
- Skirt patterns
- Default value handling
- PDF generation options

## Technical Details

- **Pattern Generation**: Uses the basic PatternGenerator from the pattern_generator package
- **PDF Export**: Uses PatternExporter with matplotlib and reportlab
- **Measurements**: Uses DefaultMeasurements for standard sizes
- **Scale**: All patterns generated at 1:1 scale in centimeters
- **A4 Page Size**: 21.0 × 29.7 cm
- **Margins**: 2.0 cm on all sides

## Tips

1. **Printing Accuracy**: After printing, measure the 10cm scale bar to ensure 100% scale
2. **Seam Allowance**: Patterns do NOT include seam allowance - add 1.5cm when cutting
3. **A4 Assembly**: Use alignment marks to tape A4 pages together accurately
4. **Paper Size**: Ensure your printer is set to A4 (not Letter) when using A4-tiled PDFs

## Requirements

- Python 3.7+
- matplotlib
- numpy
- scipy
- Pillow
- reportlab

Install with:
```bash
pip install -r requirements.txt
```

## Limitations

- Currently uses default measurements for each size
- Custom measurements require using the `generate-pattern` CLI tool
- OpenPattern integration not included in this version (uses basic patterns)

## Future Enhancements

Potential improvements:
- Custom measurement input
- More style options (coats, dresses)
- OpenPattern integration for professional patterns
- Size grading between multiple sizes
- Custom seam allowance options
- Pattern modification options
