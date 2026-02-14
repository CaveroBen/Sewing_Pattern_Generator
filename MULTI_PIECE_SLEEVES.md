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
- Upper Sleeve (Oversleeve) - back/outer piece
- Under Sleeve (Undersleeve) - front/inner piece

**How it works:**
- Splits the sleeve along the **elbow line** (not a simple vertical center)
- The split runs from back-center of cap, through the elbow, to back-center of cuff
- Split is biased toward the back: ~55-60% back, ~40-45% front
- Upper sleeve is wider at the cap (for back of arm)
- Under sleeve is narrower at cap, wider at forearm (for front of arm)
- Follows proper tailoring standards for anatomical fit

**Technical Details:**
- Cap region: Split at 60% toward back edge
- Mid/elbow region: Split at 55% toward back edge
- Cuff region: Split at 50% (centered)
- This creates proper sleeve drape and movement

**Benefits:**
- Better fit around the arm and elbow
- Follows anatomical structure of the arm
- Easier to achieve a tailored fit
- Reduces strain on fabric
- More professional appearance
- Matches standard tailoring practices

**Use cases:**
- Tailored jackets and coats
- Professional garments requiring precise fit
- Patterns where arm mobility is important
- Any garment where sleeve fit is critical

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
- Analyzes sleeve structure to identify front (narrower at cap) and back (wider at cap) edges
- Determines which side is back based on cap width measurements
- Creates offset split line following the **elbow line** from back-center of cap to back-center of cuff
- Split bias varies by region:
  - Cap: 60% toward back edge
  - Mid/elbow: 55% toward back edge
  - Cuff: 50% (centered)
- Properly assigns vertices to upper (back) vs under (front) pieces
- Returns list of piece definitions with anatomically correct proportions

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

**Two-Piece Sleeve Splitting Process:**

1. **Analyze Sleeve Geometry:**
   - Find top (cap) and bottom (cuff) of sleeve
   - Calculate sleeve height
   - Identify cap, mid (elbow), and cuff regions
   - Measure width at cap to determine front vs back

2. **Identify Front and Back:**
   - Analyze cap region to find rightmost and leftmost extents
   - Back side is typically wider at cap (extends further)
   - Determine if back is on right or left side

3. **Create Anatomical Split Line:**
   - Split follows the **elbow line**, not vertical center
   - Offset toward back: 55-60% back, 40-45% front
   - Variable bias by region:
     - Cap (top 30%): 60% toward back for proper back width
     - Mid/elbow (30-70%): 55% toward back for natural drape
     - Cuff (bottom 30%): 50% centered for symmetrical cuff
   - Creates smooth curve from back of cap to back of cuff

4. **Separate Vertices:**
   - Classify each vertex as upper (back) or under (front)
   - Uses nearest point on split line for classification
   - Maintains vertex order for proper polygon formation
   - Add split line points to both pieces for seam matching

5. **For Three-Piece:**
   - Apply two-piece split first
   - Identify cuff region (lower 20-25%)
   - Split both pieces at cuff line
   - Combine cuff portions into single piece
   - Maintain proper seam matching points

**Key Principle:**
A proper two-piece sleeve divides along anatomical lines, not geometric center. The split follows the natural curve from the back of the arm at the cap, through the elbow, to the back of the wrist. This creates:
- Upper sleeve (oversleeve): Wider at cap, covers back of arm
- Under sleeve (undersleeve): Narrower at cap, covers front of arm

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
