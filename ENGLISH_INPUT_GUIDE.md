# English Measurement Input - Quick Start Guide

## Overview

The `create_custom_measurements.py` tool makes creating custom patterns easy by accepting measurements in English instead of French technical terms.

## Why Use This Tool?

- **English Names**: No need to learn French measurement terms
- **Smart Defaults**: Start with a standard size, only change what you need
- **Interactive**: Clear prompts guide you through each measurement
- **Automatic Conversion**: Outputs JSON that works with the pattern generator

## Quick Start

### Step 1: Run the Tool

```bash
python create_custom_measurements.py
```

### Step 2: Select Base Size

The tool will ask you to choose a standard pattern size:

```
SELECT BASE PATTERN SIZE
Enter pattern size code (e.g., W36G, M44G)
  [Default: W36G, press Enter to keep]:
```

Choose a size close to your actual measurements. Its values will be used as defaults.

### Step 3: Enter Your Measurements

The tool prompts for measurements by category:

```
--- Torso ---
Do you want to modify Torso measurements? (yes/no/skip)
  [Default: yes, press Enter to keep]: yes

Bust Circumference: Bust/chest circumference
  [Default: 84.00 cm, press Enter to keep]: 90

Waist Circumference: Waist circumference
  [Default: 62.00 cm, press Enter to keep]: 68

Hip Circumference: Hip circumference (at fullest part)
  [Default: 88.00 cm, press Enter to keep]: 94
```

**Tips:**
- Press Enter to keep the default from the base size
- Type "no" or "skip" for entire categories you don't need to change
- All measurements are in centimeters

### Step 4: Generate Your Pattern

Use the created file with the pattern generator:

```bash
python interactive_generator.py --pattern bodice \
    --bespoke my_custom_measurements.json \
    --gender w
```

## Measurement Categories

### Torso
- Bust/chest circumference
- Waist circumference
- Hip circumference
- Small hip circumference
- Neck circumference

### Lengths
- Back length (nape to waist)
- Front length (shoulder to waist)
- Shoulder length
- Sleeve length (shoulder to wrist)
- Waist to floor

### Widths
- Back width (shoulder blade to shoulder blade)
- Front width (chest width)
- Neckline width

### Heights/Depths
- Armhole depth
- Bust point height
- Hip height
- Back shoulder height

### Arm Measurements
- Upper arm circumference
- Wrist circumference
- Elbow height

### Leg Measurements (for trousers)
- Thigh circumference
- Knee circumference
- Ankle circumference
- Crotch depth/rise

## Examples

### Example 1: Create Women's Bodice Measurements

```bash
python create_custom_measurements.py --pname W36G --gender w
```

Then answer the prompts to enter your measurements.

### Example 2: Create Men's Shirt Measurements

```bash
python create_custom_measurements.py --pname M44G --gender m
```

### Example 3: See All Measurement Names

```bash
python create_custom_measurements.py --reference
```

This shows the complete English-to-French mapping.

## Common Workflows

### Workflow 1: Mostly Standard Size

If you're close to a standard size:

1. Run: `python create_custom_measurements.py`
2. Choose your closest standard size
3. Answer "no" to most categories
4. Only modify the 2-3 measurements that differ
5. Result: Fast customization with minimal input

### Workflow 2: Custom Fit

If you need a truly custom fit:

1. Run: `python create_custom_measurements.py`
2. Choose any standard size as a starting point
3. Go through each category
4. Modify all key measurements (bust, waist, hip, lengths)
5. Result: Fully bespoke pattern

### Workflow 3: Multiple People

Create measurement files for different people:

```bash
# Person 1
python create_custom_measurements.py --output person1_measurements.json

# Person 2
python create_custom_measurements.py --output person2_measurements.json

# Generate patterns
python interactive_generator.py --pattern bodice --bespoke person1_measurements.json --gender w
python interactive_generator.py --pattern bodice --bespoke person2_measurements.json --gender w
```

## Output Format

The tool creates a JSON file that looks like this:

```json
{
  "_metadata": {
    "source_size": "W36G",
    "gender": "w",
    "style": "Gilewska",
    "description": "Custom body measurements based on W36G",
    "units": "centimeters",
    "note": "Created with English input, converted to French names for OpenPattern",
    "created_with": "create_custom_measurements.py"
  },
  "measurements": {
    "tour_poitrine": 90.0,
    "tour_taille": 68.0,
    "tour_bassin": 94.0,
    ...
  }
}
```

Note: The measurements use French names (`tour_poitrine`, etc.) but you entered them in English!

## Troubleshooting

### Q: I don't know some measurements

**A:** Use the defaults from the base size. Just press Enter to keep them.

### Q: Which base size should I choose?

**A:** Choose the standard size closest to your bust/chest measurement. The tool will let you adjust all other measurements.

### Q: Can I skip measurements?

**A:** Yes! Answer "no" or "skip" when asked if you want to modify a category. The defaults from the base size will be used.

### Q: What if I make a mistake?

**A:** Just run the tool again and create a new file. Or edit the JSON file to fix specific values.

## Advanced Usage

### Non-Interactive Mode

If you want to script the creation:

```bash
echo -e "no\nno\nno\nno\nno\nno\nno" | \
python create_custom_measurements.py \
    --pname W36G \
    --gender w \
    --style Gilewska \
    --output quick_measurements.json
```

This creates a file using all defaults from W36G.

### Measurement Reference

Show the complete English-French mapping:

```bash
python create_custom_measurements.py --reference
```

Output example:
```
Torso:
  bust_circumference             -> tour_poitrine                  (Bust/chest circumference)
  waist_circumference            -> tour_taille                    (Waist circumference)
  hip_circumference              -> tour_bassin                    (Hip circumference (at fullest part))
  ...
```

## Tips for Accurate Measurements

1. **Use a flexible measuring tape**: Fabric measuring tape works best
2. **Measure over appropriate undergarments**: Sports bra, etc.
3. **Stand naturally**: Don't hold your breath or pull tight
4. **Get help if possible**: Some measurements are easier with assistance
5. **Round to nearest 0.5 cm**: No need for extreme precision

## Next Steps

After creating your measurements file:

1. **Generate a pattern**: Use with `interactive_generator.py`
2. **Make a test garment**: Sew with cheap fabric first
3. **Adjust if needed**: Run the tool again with refined measurements
4. **Save for future use**: Keep your measurement file for creating multiple patterns

## Support

- See [MEASUREMENTS.md](MEASUREMENTS.md) for detailed documentation
- See [README.md](README.md) for general usage
- Run `python create_custom_measurements.py --help` for options
