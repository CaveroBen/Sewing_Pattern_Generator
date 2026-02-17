# Bespoke Measurement Files

This directory contains example JSON files for creating patterns with custom measurements.

## Overview

The measurement JSON files allow you to customize pattern parameters while using OpenPattern's standard size tables as a base. This "bespoke" mode lets you:

- Start with a standard size (e.g., W36G, M44G)
- Adjust specific parameters like ease, lengths, and fit preferences
- Create personalized patterns without needing complete body measurements

## File Structure

Each JSON file contains:
- `pname`: The base size code from OpenPattern's standard sizing (e.g., "W36G", "M44D")
- Additional parameters specific to the pattern type

## Example Files

### measurements_bodice_example.json
Bodice pattern with custom ease and spacing:
```json
{
  "pname": "W36G",
  "ease": 10,
  "hip": false,
  "Back_Front_space": 5
}
```

Parameters:
- `pname`: Base size (W36G = Women's size 36, Gilewska style)
- `ease`: Extra room in cm for comfort (default: 8)
- `hip`: Include hip measurements (default: false)
- `Back_Front_space`: Space between back and front pieces in cm (default: 4)

### measurements_shirt_example.json
Shirt pattern with custom fit and length:
```json
{
  "pname": "M44G",
  "ease": 2,
  "lower_length": 30,
  "hip": false,
  "Back_Front_space": 14,
  "collar_ease": 1.5,
  "sleeve_lowering": 3,
  "side_ease": 6,
  "shoulder_ease": 1,
  "button_overlap": 2.5
}
```

Parameters:
- `pname`: Base size (M44G = Men's size 44, Gilewska style)
- `ease`: General ease in cm (default: 0)
- `lower_length`: Length of lower part in cm (default: 25)
- `hip`: Include hip measurements (default: false)
- `Back_Front_space`: Back to front spacing in cm (default: 12)
- `collar_ease`: Extra room in collar in cm (default: 1)
- `sleeve_lowering`: How much to lower sleeve in cm (default: 3)
- `side_ease`: Side seam ease in cm (default: 4)
- `shoulder_ease`: Shoulder ease in cm (default: 1)
- `button_overlap`: Button overlap width in cm (default: 2)

### measurements_waistcoat_example.json
Waistcoat pattern with custom style:
```json
{
  "pname": "M44G",
  "ease": 10,
  "wc_style": "Classical",
  "overlap": false
}
```

Parameters:
- `pname`: Base size (M44G = Men's size 44, Gilewska style)
- `ease`: Extra room in cm (default: 8)
- `wc_style`: Waistcoat style - "Classical" or other options (default: "Classical")
- `overlap`: Whether fronts overlap (default: false)

## Usage

### Command Line
```bash
# Use bespoke measurements for a shirt
python interactive_generator.py --pattern shirt \
    --bespoke measurements_shirt_example.json \
    --gender m \
    --style Gilewska

# Use bespoke measurements for a bodice
python interactive_generator.py --pattern bodice \
    --bespoke measurements_bodice_example.json \
    --gender w \
    --style Gilewska
```

### Interactive Mode
```bash
python interactive_generator.py
# Then select:
# - Pattern type: shirt
# - Size mode: bespoke
# - Measurements file: measurements_shirt_example.json
# - Gender: m
# - Style: Gilewska
```

## Creating Your Own Measurement Files

1. Start with one of the example files
2. Keep the `pname` field with a valid OpenPattern size code
3. Adjust only the parameters you want to customize
4. Save with a descriptive name (e.g., `my_custom_shirt.json`)
5. Use with the interactive generator:
   ```bash
   python interactive_generator.py --pattern shirt --bespoke my_custom_shirt.json --gender m
   ```

## Standard Size Codes

OpenPattern uses size codes like:
- **Women's sizes**: W36G, W38G, W40G, W42G, etc.
- **Men's sizes**: M44G, M46G, M48G, M50G, etc.
- **Style codes**: 
  - G = Gilewska
  - C = Chiappetta
  - D = Donnanno

Examples:
- W36G = Women's size 36, Gilewska style
- M44D = Men's size 44, Donnanno style
- W40C = Women's size 40, Chiappetta style

## Notes

- All measurements are in centimeters
- The `pname` should always use a valid standard size as the base
- Only parameters specific to each pattern type will be used
- Parameters not in the JSON will use their default values
- Boolean values should be `true` or `false` (lowercase, no quotes)
- Numeric values can be integers or decimals (no quotes)
