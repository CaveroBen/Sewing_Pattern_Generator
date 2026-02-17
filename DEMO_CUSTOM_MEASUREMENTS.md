# Custom Body Measurements - Demo & Guide

## Overview

This guide demonstrates how to use the new custom body measurements feature for true bespoke pattern generation.

## Quick Start

### 1. Extract Standard Measurements

```bash
# Extract women's size 36 measurements as a template
python extract_measurements.py --pname W36G --gender w --output my_measurements.json
```

**Output:**
```
Extracting measurements for W36G (w, Gilewska)...
✓ Measurement template saved to: my_measurements.json
  Contains 35 body measurements
```

### 2. View the Measurements

The extracted JSON contains:
```json
{
  "_metadata": {
    "source_size": "W36G",
    "gender": "w",
    "style": "Gilewska",
    "description": "Standard body measurements for W36G",
    "units": "centimeters",
    "note": "Modify these values to create custom-fitted patterns"
  },
  "measurements": {
    "tour_poitrine": 84.0,      // Bust circumference
    "tour_taille": 62.0,        // Waist circumference
    "tour_bassin": 88.0,        // Hip circumference
    "longueur_dos": 41.5,       // Back length
    "longueur_devant": 44.8,    // Front length
    "longueur_epaule": 13.6,    // Shoulder length
    "carrure_dos": 35.0,        // Back width
    "carrure_devant": 33.5,     // Front width
    ... 27 more measurements ...
  }
}
```

### 3. Customize Measurements

Edit `my_measurements.json` to match your actual body:

**Example modifications:**
```json
{
  "_metadata": {
    "description": "My custom body measurements - based on W36G"
  },
  "measurements": {
    "tour_poitrine": 90.0,      // Changed from 84.0
    "tour_taille": 68.0,        // Changed from 62.0
    "tour_bassin": 94.0,        // Changed from 88.0
    "longueur_dos": 43.0,       // Changed from 41.5 (longer torso)
    ... rest unchanged ...
  }
}
```

### 4. Generate Custom Pattern

```bash
python interactive_generator.py --pattern bodice \
    --bespoke my_measurements.json \
    --gender w \
    --style Gilewska
```

**Output:**
```
============================================================
Generating CUSTOM BODICE pattern
============================================================
  Using custom body measurements
  Base size: W36G (measurements will be replaced)
  Gender: w
  Style: Gilewska
  Total measurements: 35

  Applying 35 custom measurements...

✓ Pattern saved: output/custom_bodice_W36G.pdf

Note: Custom body measurements have been applied.
```

## Comparison: Parameter-Only vs Full Measurements

### Parameter-Only Mode (Simple)

**File: measurements_bodice_example.json**
```json
{
  "pname": "W36G",
  "ease": 10,
  "hip": false,
  "Back_Front_space": 5
}
```

**Effect:** Adjusts pattern parameters but body measurements come from W36G

**Usage:**
```bash
python interactive_generator.py --pattern bodice \
    --bespoke measurements_bodice_example.json --gender w
```

### Full Measurements Mode (Advanced Bespoke)

**File: custom_measurements.json**
```json
{
  "_metadata": {
    "source_size": "W36G",
    "description": "Custom measurements"
  },
  "measurements": {
    "tour_poitrine": 90.0,
    "tour_taille": 68.0,
    ... 33 more measurements ...
  }
}
```

**Effect:** Replaces all body measurements with custom values

**Usage:**
```bash
python interactive_generator.py --pattern bodice \
    --bespoke custom_measurements.json --gender w
```

## Key Measurements Explained

### Primary Body Measurements

| Measurement | English | Description |
|------------|---------|-------------|
| tour_poitrine | Bust/Chest | Fullest part of bust/chest |
| tour_taille | Waist | Natural waistline |
| tour_bassin | Hip | Fullest part of hips |
| tour_encolure | Neck | Neck circumference |

### Length Measurements

| Measurement | English | Description |
|------------|---------|-------------|
| longueur_dos | Back length | Nape to waist back |
| longueur_devant | Front length | Shoulder to waist front |
| longueur_epaule | Shoulder | Shoulder point to neck |
| longueur_manche | Sleeve | Shoulder to wrist |

### Width Measurements

| Measurement | English | Description |
|------------|---------|-------------|
| carrure_dos | Back width | Shoulder blade to shoulder blade |
| carrure_devant | Front width | Chest width |
| largeur_encolure | Neckline width | Side of neck to side of neck |

### Height/Depth Measurements

| Measurement | English | Description |
|------------|---------|-------------|
| hauteur_emmanchure | Armhole depth | Shoulder to underarm |
| hauteur_poitrine | Bust height | Shoulder to bust point |
| hauteur_bassin | Hip height | Waist to hip |

## Tips for Success

1. **Start with a close standard size** - Choose a base size (W36G, W38G, etc.) that's closest to your measurements
2. **Measure accurately** - Use a flexible measuring tape and follow standard measurement techniques
3. **Test with muslin** - Make a test garment first to verify fit
4. **Adjust gradually** - Start with primary measurements (bust, waist, hip) before fine-tuning others
5. **Keep records** - Save your custom measurement files for future use

## Troubleshooting

### Q: Can I use custom measurements with all pattern types?

**A:** Yes! Works with bodice, skirt, trousers, shirt. Waistcoat only supports men's sizes.

### Q: Do I need to provide all 35 measurements?

**A:** No, but it's recommended. Start with a standard size template and modify only what you need. Unmodified measurements will use the template values.

### Q: How accurate is the custom fitting?

**A:** The pattern measurements are replaced, but some derived calculations may still reference the base size. For best results, choose a base size close to your actual measurements.

## Example Workflow

```bash
# 1. Extract multiple sizes to compare
python extract_measurements.py --pname W36G --output compare_W36G.json
python extract_measurements.py --pname W40G --output compare_W40G.json

# 2. Choose closest size and customize
cp compare_W36G.json my_size.json
# Edit my_size.json with your measurements

# 3. Generate multiple patterns
python interactive_generator.py --pattern bodice --bespoke my_size.json --gender w
python interactive_generator.py --pattern skirt --bespoke my_size.json --gender w
python interactive_generator.py --pattern shirt --bespoke my_size.json --gender w

# 4. Review and adjust
# If needed, modify measurements and regenerate
```

## Support

For more information:
- See [MEASUREMENTS.md](MEASUREMENTS.md) for complete documentation
- See [README.md](README.md) for general usage
- Run `python extract_measurements.py --help` for extraction options
- Run `python interactive_generator.py --help` for generation options
