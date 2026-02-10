# Pattern Generation Approaches

## Simple OpenPattern Usage (Recommended)

The simplest and most reliable way to use OpenPattern is directly with standard sizes:

```python
import matplotlib.pyplot as plt
import OpenPattern as OP

# Use standard size codes
p = OP.Basic_Bodice(
    pname="W36G",      # Women, size 36, Gilewska method
    gender='w',
    style='Gilewska'
)

p.draw()
plt.show()
```

**Why this works:**
- OpenPattern has built-in measurements for standard sizes
- No complex measurement conversion needed
- Proven, tested code from OpenPattern library
- Minimal lines of code

**Standard size codes:**
- Women: "W36G", "W38G", "W40G", etc.
- Men: "M38G", "M40G", "M42G", etc.
- G = Gilewska method

## Complex Wrapper Approach (Not Recommended)

The `OpenPatternGenerator` class attempts to wrap OpenPattern with custom measurements, but this requires:
- Converting measurements to French naming conventions
- Complex measurement mapping logic
- Additional error handling
- More points of failure

**Issues with the wrapper:**
- OpenPattern expects specific measurement keys (e.g., "tour_poitrine" for bust)
- Custom measurement names don't map correctly
- Additional complexity without clear benefits

## Recommendation

For users who want professional patterns:
1. **Use OpenPattern directly** with standard sizes (as shown in `examples/simple_bodice.py`)
2. For custom measurements with OpenPattern, refer to OpenPattern's own documentation
3. For simple patterns without OpenPattern, use the basic `PatternGenerator` class

The simple approach reduces complexity and produces reliable results.
