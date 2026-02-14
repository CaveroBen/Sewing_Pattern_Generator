# Pattern Transformation Guide

## Overview

The Sewing Pattern Generator now supports transforming basic patterns into more complex designs. This feature allows you to start with a basic pattern (like a bodice) and add elements to it (like sleeves) to create a complete garment pattern.

## Supported Transformations

### Bodice → Bodice with Sleeves

Transform a basic bodice pattern by adding fitted sleeves. The sleeves are automatically drafted to fit the armhole of the bodice.

**Output Format:** 
- **Basic sleeve (1-piece):** 2-page PDF with bodice and sleeve
- **Two-piece sleeve:** 5-page PDF with bodice, reference sleeve, overview, and individual pieces
- **Three-piece sleeve:** 6-page PDF with bodice, reference sleeve, overview, and individual pieces

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

#### Multi-Piece Sleeves

**Two-Piece Sleeve:**
- Upper sleeve (back) and under sleeve (front) pieces
- Provides better fit and shaping around the arm
- Easier to achieve a tailored fit
- Suitable for most fitted garments

**Three-Piece Sleeve (Chanel-Style):**
- Upper sleeve, under sleeve, and separate cuff piece
- Allows for precise wrist shaping
- Enables positioning of buttons/fasteners on top of the wrist
- Ideal for Chanel jackets and high-end tailored garments
- The cuff piece provides additional structure and design opportunities

## Usage

### Command Line Interface

#### Basic Bodice with Sleeves

```bash
# Generate women's bodice with basic single-piece sleeves (default)
python generate_patterns.py --type bodice --size W36G --add-sleeves

# Generate with two-piece sleeves for better fit
python generate_patterns.py --type bodice --size W36G --add-sleeves --sleeve-pieces 2

# Generate with three-piece Chanel-style sleeves
python generate_patterns.py --type bodice --size W36G --add-sleeves --sleeve-pieces 3

# Generate with specific sleeve style
python generate_patterns.py --type bodice --size W36G --add-sleeves --sleeve-style Chiappetta

# Generate men's bodice with two-piece sleeves
python generate_patterns.py --type bodice --size M44G --gender m --add-sleeves --sleeve-pieces 2
```

#### Options

- `--add-sleeves`: Enable sleeve transformation (only for bodice patterns)
- `--sleeve-style {Gilewska,Chiappetta}`: Choose sleeve style (optional, defaults to bodice style)
- `--sleeve-pieces {1,2,3}`: Number of pieces for sleeve (optional, defaults to 1)
  - `1`: Basic single-piece sleeve
  - `2`: Two-piece sleeve (upper and under)
  - `3`: Three-piece Chanel-style sleeve with cuff

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
    "sleeve_style": "Gilewska",
    "sleeve_pieces": 2
  }
}
```

For three-piece Chanel-style sleeve:

```json
{
  "type": "bodice",
  "name": "W38G",
  "style": "Gilewska",
  "gender": "w",
  "transformations": {
    "add_sleeves": true,
    "sleeve_style": "Gilewska",
    "sleeve_pieces": 3
  }
}
```

Then generate:

```bash
python generate_patterns.py --json your_config.json
```

## Examples

### Example 1: Women's Bodice with Basic Sleeves

**Command:**
```bash
python generate_patterns.py --type bodice --size W38G --add-sleeves
```

**Output:** `output/bodice_W38G_with_sleeves.pdf` (2-page PDF: bodice + sleeves)

### Example 2: Women's Bodice with Two-Piece Sleeves

**Command:**
```bash
python generate_patterns.py --type bodice --size W36G --add-sleeves --sleeve-pieces 2
```

**Output:** `output/bodice_W36G_with_sleeves_2piece.pdf` (5-page PDF)
- Page 1: Bodice pattern
- Page 2: Original sleeve (reference)
- Page 3: Two-piece overview
- Pages 4-5: Upper and under sleeve pieces

### Example 3: Women's Bodice with Three-Piece Chanel-Style Sleeves

**Command:**
```bash
python generate_patterns.py --type bodice --size W38G --add-sleeves --sleeve-pieces 3
```

**Output:** `output/bodice_W38G_with_sleeves_3piece.pdf` (6-page PDF)
- Page 1: Bodice pattern
- Page 2: Original sleeve (reference)
- Page 3: Three-piece overview
- Pages 4-6: Upper sleeve, under sleeve, and cuff pieces

### Example 4: Using JSON Configuration for Two-Piece Sleeve

**File: test_two_piece_sleeve.json**
```json
{
  "type": "bodice",
  "name": "W36G",
  "style": "Gilewska",
  "gender": "w",
  "transformations": {
    "add_sleeves": true,
    "sleeve_style": "Gilewska",
    "sleeve_pieces": 2
  },
  "note": "Two-piece sleeve for better fit and shaping"
}
```

**Command:**
```bash
python generate_patterns.py --json test_two_piece_sleeve.json
```

### Example 5: Using JSON Configuration for Three-Piece Sleeve

**File: test_three_piece_sleeve.json**
```json
{
  "type": "bodice",
  "name": "W38G",
  "style": "Gilewska",
  "gender": "w",
  "transformations": {
    "add_sleeves": true,
    "sleeve_style": "Gilewska",
    "sleeve_pieces": 3
  },
  "note": "Three-piece Chanel-style sleeve with cuff"
}
```

**Command:**
```bash
python generate_patterns.py --json test_three_piece_sleeve.json
```

## Technical Details

### How Sleeve Transformation Works

1. A basic bodice pattern is generated first
2. The sleeve method is called on the bodice object
3. The sleeve is automatically fitted to the armhole using OpenPattern's built-in methods
4. For multi-piece sleeves:
   - The basic sleeve pattern is split algorithmically into 2 or 3 pieces
   - Split lines follow the natural curves of the sleeve
   - Each piece is labeled with grainlines and notches
   - Pieces are saved as separate PDF pages for easy printing

### Multi-Piece Sleeve Algorithm

**Two-Piece Sleeve:**
- Splits sleeve along the vertical centerline
- Creates upper sleeve (back/outer) and under sleeve (front/inner)
- Allows for better shaping around the elbow
- Provides easier fitting adjustments

**Three-Piece Sleeve:**
- First splits into upper and under pieces (like two-piece)
- Then separates the lower 20-25% to create a cuff piece
- Cuff piece wraps around the wrist for precise shaping
- Button placement can be positioned on top of wrist (Chanel technique)

### Style Compatibility

| Bodice Style | Sleeve Style | Pieces | Women | Men | Notes |
|--------------|--------------|--------|--------|-----|-------|
| Gilewska     | Gilewska     | 1-3    | ✅     | ✅   | Recommended combination |
| Gilewska     | Chiappetta   | 1-3    | ✅     | ✅   | Works well for all patterns |
| Chiappetta   | Gilewska     | 1-3    | ✅     | ✅   | Good fallback option |
| Chiappetta   | Chiappetta   | 1-3    | ✅     | ✅   | Traditional approach |

### Error Handling

The transformation system includes automatic fallback:
- If a requested sleeve style is not available for a gender, it falls back to Gilewska
- If a sleeve method fails, it attempts Gilewska style as a backup
- If multi-piece sleeve generation fails, falls back to basic sleeve
- All errors are logged with helpful messages

## Benefits of Multi-Piece Sleeves

**Two-Piece Sleeves:**
- Better fit around the arm and elbow
- Easier to adjust for individual proportions
- More professional appearance
- Reduces pulling and strain on fabric

**Three-Piece Sleeves:**
- All benefits of two-piece sleeves
- Precise wrist shaping and fit
- Ability to position cuff details (buttons, zippers) on top of wrist
- Essential for Chanel-style jackets
- Allows for decorative cuff treatments
- Better drape and movement

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
