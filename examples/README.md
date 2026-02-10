# Example Measurements and Scripts

This directory contains example measurement files in JSON format and demonstration scripts.

## Files

- `mens_medium.json`: Default men's medium measurements (chest 38-40")
- `womens_medium.json`: Default women's medium measurements (UK 12-14)
- `openpattern_example.py`: Example script demonstrating OpenPattern integration

## Usage

### Using Example Measurements

```bash
# Use example measurements
generate-pattern shirt --measurements examples/mens_medium.json

# Create your own measurements file
cp examples/mens_medium.json my_measurements.json
# Edit my_measurements.json with your actual measurements
generate-pattern shirt --measurements my_measurements.json
```

### Running the OpenPattern Example

```bash
# Run the OpenPattern demonstration script
python examples/openpattern_example.py
```

This script demonstrates:
- How to check if OpenPattern is installed
- How to use OpenPatternGenerator for formal pattern drafting
- Fallback to basic generator if OpenPattern is not available

## How to Take Measurements

### General Tips
- Use a soft measuring tape
- Wear fitted clothing or underwear
- Stand naturally, don't hold your breath
- Have someone help you for accuracy
- Measure in centimeters

### Taking Each Measurement

**Chest/Bust**: Measure around the fullest part of the chest, keeping the tape horizontal and comfortable (not tight).

**Waist**: Measure around the natural waistline (smallest part of torso, usually just above belly button).

**Hip**: Measure around the fullest part of the hips and buttocks.

**Shoulder Width**: Measure from shoulder point to shoulder point across the back.

**Neck**: Measure around the base of the neck where a shirt collar would sit.

**Sleeve Length**: Measure from shoulder point to wrist bone with arm slightly bent.

**Bicep**: Measure around the fullest part of the upper arm.

**Wrist**: Measure around the wrist bone.

**Inseam**: Measure from crotch to ankle along the inside of the leg.

**Outseam**: Measure from waist to ankle along the outside of the leg.

**Rise**: Measure from waist (back) down through crotch to waist (front).

**Nape to Waist**: Measure from the base of the neck down the spine to the waistline.
