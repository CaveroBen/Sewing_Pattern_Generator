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
Waistcoat pattern with custom style (men's sizes only):
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

**Note**: Waistcoat patterns currently only support men's sizes due to OpenPattern library limitations.

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

### Option 1: Parameter-Only Customization (Simple)

1. Start with one of the example files
2. Keep the `pname` field with a valid OpenPattern size code
3. Adjust only the parameters you want to customize (ease, lengths, etc.)
4. Save with a descriptive name (e.g., `my_custom_shirt.json`)
5. Use with the interactive generator:
   ```bash
   python interactive_generator.py --pattern shirt --bespoke my_custom_shirt.json --gender m
   ```

### Option 2: Full Body Measurements (Advanced - True Bespoke)

For truly custom-fitted patterns, you can provide complete body measurements:

1. Extract a standard size template as a starting point:
   ```bash
   python extract_measurements.py --pname W36G --gender w --output my_measurements.json
   ```

2. Edit the JSON file and modify the measurements in the `measurements` section:
   ```json
   {
     "_metadata": {
       "source_size": "W36G",
       "description": "My custom body measurements"
     },
     "measurements": {
       "tour_poitrine": 90.0,
       "tour_taille": 68.0,
       "tour_bassin": 94.0,
       ...
     }
   }
   ```

3. Use the custom measurements file:
   ```bash
   python interactive_generator.py --pattern bodice --bespoke my_measurements.json --gender w
   ```

**Important Notes for Full Body Measurements:**
- This provides the most accurate custom fitting
- All 35 body measurements can be customized
- The pattern is based on a standard size but measurements are overridden
- Some derived calculations may still use the base size
- Choose a base size (source_size) close to your actual measurements for best results

### Extracting Standard Measurements

Use the `extract_measurements.py` utility to see what measurements OpenPattern uses:

```bash
# List available sizes
python extract_measurements.py --list

# Extract women's size 36
python extract_measurements.py --pname W36G --gender w --output measurements_W36G.json

# Extract men's size 44
python extract_measurements.py --pname M44G --gender m --output measurements_M44G.json
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

## Body Measurements Reference

When using full body measurements (Option 2), here are the key measurements used:

### Torso Measurements
- `tour_poitrine` - Bust/chest circumference
- `tour_taille` - Waist circumference
- `tour_bassin` - Hip circumference
- `tour_petites_hanches` - Small hip circumference
- `tour_encolure` - Neck circumference

### Lengths
- `longueur_dos` - Back length (nape to waist)
- `longueur_devant` - Front length (shoulder to waist)
- `longueur_taille_terre` - Total height (waist to floor)
- `longueur_epaule` - Shoulder length
- `longueur_manche` - Sleeve length

### Widths
- `carrure_dos` - Back width (shoulder blade to shoulder blade)
- `carrure_devant` - Front width (chest width)
- `largeur_encolure` - Neckline width

### Heights/Depths
- `hauteur_emmanchure` - Armhole depth
- `hauteur_poitrine` - Bust point height
- `hauteur_bassin` - Hip height
- `hauteur_carrure` - Back shoulder height
- `profondeur_encolure_dos` - Back neckline depth
- `profondeur_encolure_devant` - Front neckline depth

### Arm Measurements
- `tour_bras` - Upper arm circumference
- `tour_poignet` - Wrist circumference
- `hauteur_coude` - Elbow height

### Leg Measurements (for trousers)
- `tour_cuisse` - Thigh circumference
- `tour_genou` - Knee circumference
- `tour_cheville` - Ankle circumference
- `fourche` - Crotch depth/rise
- `montant` - Crotch measurement

Use `extract_measurements.py` to see all 35+ measurements with their values for any standard size.
