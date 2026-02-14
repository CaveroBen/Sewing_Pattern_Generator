# Multi-Piece Sleeve Implementation

## Overview

This document describes the implementation of two-piece and three-piece sleeve support in the Sewing Pattern Generator, addressing the requirement for multi-piece sleeves that introduce curvature and better shaping, particularly for Chanel-style jackets.

## Problem Statement

> "Is it possible to do a two piece or even three piece sleeve? Multiple piece sleeves are used to introduce curvature, with the three piece sleeve allows for shaping of the sleeve and moves the button up part of the cuff to be placed on top of the wrist, this is important for the Chanel jacket for example."

## Solution

### Implementation Approach

Since OpenPattern doesn't have native two-piece or three-piece sleeve methods, we implemented an algorithmic approach that:

1. Generates a basic fitted sleeve using OpenPattern's existing methods
2. Splits the sleeve pattern into multiple pieces algorithmically
3. Adds appropriate notches, grainlines, and labels to each piece
4. Outputs each piece as a separate PDF page for easy printing

### Sleeve Types Supported

#### 1. Two-Piece Sleeve

**Components:**
- Upper Sleeve (back/outer piece)
- Under Sleeve (front/inner piece)

**How it works:**
- Splits the sleeve along a vertical centerline
- The split follows the natural curve of the sleeve cap down to the cuff
- Each piece includes seam allowance for joining

**Benefits:**
- Better fit around the arm and elbow
- Easier to achieve a tailored fit
- Reduces strain on fabric
- More professional appearance

**Use cases:**
- Tailored jackets and coats
- Professional garments requiring precise fit
- Patterns where arm mobility is important

#### 2. Three-Piece Sleeve (Chanel-Style)

**Components:**
- Upper Sleeve (back/outer piece - top portion)
- Under Sleeve (front/inner piece - top portion)
- Cuff Piece (wrist shaping piece)

**How it works:**
- First splits into upper and under pieces (like two-piece)
- Then separates the lower 20-25% to create a dedicated cuff piece
- The cuff piece wraps around the wrist for precise shaping

**Benefits:**
- All benefits of two-piece sleeves
- Precise wrist shaping and fit
- Ability to position buttons/fasteners on top of wrist
- Essential for Chanel-style jackets
- Allows for decorative cuff treatments
- Better drape and movement at the wrist

**Use cases:**
- Chanel jackets (primary use case)
- High-end tailored garments
- Jackets with decorative cuff details
- Patterns requiring precise wrist button placement

## Usage

### Command Line Interface

```bash
# Generate bodice with two-piece sleeves
python generate_patterns.py --type bodice --size W36G --add-sleeves --sleeve-pieces 2

# Generate bodice with three-piece Chanel-style sleeves
python generate_patterns.py --type bodice --size W36G --add-sleeves --sleeve-pieces 3

# Combine with other options
python generate_patterns.py --type bodice --size W38G --gender w --style Gilewska \
    --add-sleeves --sleeve-pieces 3 --sleeve-style Gilewska
```

### JSON Configuration

**Two-Piece Sleeve:**
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

**Three-Piece Sleeve:**
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

## PDF Output Structure

### Two-Piece Sleeve (5 pages)
1. **Page 1:** Bodice pattern
2. **Page 2:** Original single-piece sleeve (reference)
3. **Page 3:** Two-piece sleeve overview (all pieces together)
4. **Page 4:** Upper Sleeve piece with labels and grainline
5. **Page 5:** Under Sleeve piece with labels and grainline

### Three-Piece Sleeve (6 pages)
1. **Page 1:** Bodice pattern
2. **Page 2:** Original single-piece sleeve (reference)
3. **Page 3:** Three-piece sleeve overview (all pieces together)
4. **Page 4:** Upper Sleeve (Back) piece with labels and grainline
5. **Page 5:** Under Sleeve (Front) piece with labels and grainline
6. **Page 6:** Cuff Piece with labels and grainline

## Technical Implementation

### Key Functions

#### `split_sleeve_into_pieces(sleeve_vertices, num_pieces)`
Main entry point that routes to appropriate splitting function based on `num_pieces`.

#### `_create_two_piece_sleeve(vertices, top_y, bottom_y, sleeve_height)`
- Analyzes sleeve vertices to find the approximate centerline
- Splits vertices into left (upper) and right (under) groups
- Adds split line to both pieces for proper seam matching
- Returns list of piece definitions with vertices and metadata

#### `_create_three_piece_sleeve(vertices, top_y, bottom_y, sleeve_height)`
- Calls `_create_two_piece_sleeve()` first
- Identifies cuff region (lower 20-25% of sleeve)
- Splits both upper and under pieces at cuff line
- Combines cuff portions into single cuff piece
- Returns list of three piece definitions

#### `draw_multi_piece_sleeve(pieces, title)`
- Creates visualization showing all pieces together
- Uses different colors for each piece
- Adds labels, grainlines, and notches
- Returns matplotlib figure for PDF output

### Algorithm Details

**Sleeve Splitting Process:**

1. **Analyze Sleeve Geometry:**
   - Find top (cap) and bottom (cuff) of sleeve
   - Calculate sleeve height
   - Identify center points at various heights

2. **Create Split Line:**
   - Sample points along the vertical center of the sleeve
   - Create smooth split line following natural curve
   - Ensure split line extends from cap to cuff

3. **Separate Vertices:**
   - Classify each vertex as left or right of split line
   - Maintain vertex order for proper polygon formation
   - Add split line points to both pieces

4. **For Three-Piece:**
   - Identify cuff region (lower 20-25%)
   - Split both pieces at cuff line
   - Combine cuff portions into single piece
   - Maintain proper seam matching points

## Testing

### Test Files Included

- `test_two_piece_sleeve.json` - Configuration for two-piece sleeve
- `test_three_piece_sleeve.json` - Configuration for three-piece Chanel sleeve

### Verification Commands

```bash
# Test two-piece
python generate_patterns.py --json test_two_piece_sleeve.json

# Test three-piece
python generate_patterns.py --json test_three_piece_sleeve.json

# Verify output
ls -lh output/*.pdf
```

## Chanel Jacket Application

The three-piece sleeve is particularly important for Chanel-style jackets because:

1. **Button Placement:** The separate cuff piece allows buttons or fasteners to be positioned on top of the wrist rather than on the side, which is both functional and aesthetically important.

2. **Wrist Shaping:** The cuff piece provides precise shaping around the wrist without affecting the upper sleeve fit.

3. **Construction:** The three-piece construction allows for easier adjustment during fitting and better control over the sleeve shape.

4. **Professional Finish:** This technique is a hallmark of high-quality tailoring and produces a more refined, professional appearance.

## Future Enhancements

Potential improvements for future versions:

1. **Adjustable Split Ratios:** Allow users to customize where the sleeve is split
2. **Ease Distribution:** Add customizable ease to specific pieces
3. **Decorative Elements:** Built-in support for cuff details, vents, or pleats
4. **Custom Split Lines:** Allow users to define custom split locations
5. **Notch Placement:** More sophisticated notch placement for easier assembly

## References

- Chanel jacket construction techniques
- Professional patternmaking methods
- Tailoring principles for multi-piece sleeves
- OpenPattern library documentation

---

*Implementation Date: February 2026*
*Version: 1.0*
