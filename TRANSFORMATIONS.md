# Pattern Transformation Guide

## Overview

The Sewing Pattern Generator now supports transforming basic patterns into more complex designs. This feature allows you to start with a basic pattern (like a bodice) and add elements to it (like sleeves) to create a complete garment pattern.

## Supported Transformations

### Bodice → Bodice with Sleeves

Transform a basic bodice pattern by adding fitted sleeves. The sleeves are automatically drafted to fit the armhole of the bodice.

**Output Format:** When sleeves are added, the pattern is saved as a 2-page PDF:
- **Page 1:** Bodice pattern
- **Page 2:** Sleeve pattern

This allows you to print each pattern piece separately or view them together in a single document.

#### Available Sleeve Styles

1. **Gilewska Sleeves**
   - Classic fitted sleeve design
   - Available for both women's and men's patterns
   - Based on Theresa Gilewska's pattern drafting method
   - Best for: Standard fitted garments

2. **Chiappetta Sleeves**
   - Armhole-based sleeve construction
   - Primarily designed for men's patterns
   - Based on Jacqueline Chiappetta's drafting method
   - Best for: Traditional menswear, structured garments

## Usage

### Command Line Interface

#### Basic Bodice with Sleeves

```bash
# Generate women's bodice with Gilewska sleeves (default)
python generate_patterns.py --type bodice --size W36G --add-sleeves

# Generate with specific sleeve style
python generate_patterns.py --type bodice --size W36G --add-sleeves --sleeve-style Chiappetta

# Generate men's bodice with sleeves
python generate_patterns.py --type bodice --size M44G --gender m --add-sleeves
```

#### Options

- `--add-sleeves`: Enable sleeve transformation (only for bodice patterns)
- `--sleeve-style {Gilewska,Chiappetta}`: Choose sleeve style (optional, defaults to bodice style)

### JSON Configuration

Include a `transformations` section in your JSON file:

```json
{
  "type": "bodice",
  "name": "W36G",
  "style": "Gilewska",
  "gender": "w",
  "transformations": {
    "add_sleeves": true,
    "sleeve_style": "Gilewska"
  }
}
```

Then generate:

```bash
python generate_patterns.py --json your_config.json
```

## Examples

### Example 1: Women's Bodice with Gilewska Sleeves

**Command:**
```bash
python generate_patterns.py --type bodice --size W38G --add-sleeves
```

**Output:** `output/bodice_W38G_with_sleeves.pdf` (2-page PDF: bodice + sleeves)

### Example 2: Women's Bodice with Chiappetta Sleeves

**Command:**
```bash
python generate_patterns.py --type bodice --size W40G --add-sleeves --sleeve-style Chiappetta
```

**Output:** `output/bodice_W40G_with_sleeves.pdf` (2-page PDF: bodice + sleeves)

### Example 3: Men's Bodice with Sleeves

**Command:**
```bash
python generate_patterns.py --type bodice --size M44G --gender m --add-sleeves
```

**Output:** `output/bodice_M44G_with_sleeves.pdf` (2-page PDF: bodice + sleeves)

### Example 4: Using JSON Configuration

**File: custom_bodice.json**
```json
{
  "type": "bodice",
  "name": "W36G",
  "style": "Gilewska",
  "gender": "w",
  "transformations": {
    "add_sleeves": true,
    "sleeve_style": "Gilewska"
  },
  "note": "Custom bodice with fitted sleeves"
}
```

**Command:**
```bash
python generate_patterns.py --json custom_bodice.json
```

## Technical Details

### How Sleeve Transformation Works

1. A basic bodice pattern is generated first
2. The sleeve method is called on the bodice object
3. The sleeve is automatically fitted to the armhole using OpenPattern's built-in methods
4. Both bodice and sleeve pieces are drawn on the same pattern
5. The complete pattern is saved as a PDF

### Style Compatibility

| Bodice Style | Sleeve Style | Women | Men | Notes |
|--------------|--------------|--------|-----|-------|
| Gilewska     | Gilewska     | ✅     | ✅   | Recommended combination |
| Gilewska     | Chiappetta   | ✅     | ✅   | Works well for all patterns |
| Chiappetta   | Gilewska     | ✅     | ✅   | Good fallback option |
| Chiappetta   | Chiappetta   | ✅     | ✅   | Traditional approach |

### Error Handling

The transformation system includes automatic fallback:
- If a requested sleeve style is not available for a gender, it falls back to Gilewska
- If a sleeve method fails, it attempts Gilewska style as a backup
- All errors are logged with helpful messages

## Future Transformations

The transformation framework is designed to be extensible. Potential future additions:

- Collar transformations
- Pocket additions
- Dart manipulations
- Skirt length variations
- Trouser modifications

## Sample Files

The repository includes these sample JSON files for testing transformations:

- `test_bodice_with_sleeves.json` - Women's bodice with Gilewska sleeves
- `test_mens_bodice_sleeves.json` - Men's bodice with Gilewska sleeves

## Troubleshooting

**Q: My sleeve generation failed with an error**
A: Some sleeve styles may not work with all bodice styles. The system will automatically try Gilewska style as a fallback.

**Q: Can I add sleeves to skirt or trouser patterns?**
A: Currently, sleeve transformations only work with bodice patterns. The `--add-sleeves` flag is ignored for other pattern types.

**Q: The sleeve doesn't fit my bodice**
A: The sleeve fitting is automatic and based on OpenPattern's calculations. Make sure you're using compatible sizes and styles.

**Q: How do I know which sleeve style to use?**
A: Gilewska sleeves work well for most applications. Try different styles to see which gives the best result for your specific needs.
