# OpenPattern Examples

This directory contains example scripts demonstrating how to generate different types of sewing patterns using the OpenPattern library.

## Examples

### Bodice Pattern
```bash
python bodice_example.py
```
Generates a women's basic bodice pattern using the Gilewska drafting style.

### Skirt Pattern
```bash
python skirt_example.py
```
Generates a women's basic skirt pattern using the Chiappetta drafting style.

### Trousers Pattern
```bash
python trousers_example.py
```
Generates a men's basic trousers pattern using the Donnanno drafting style.

## Output

Each example will:
1. Generate the pattern using OpenPattern
2. Save the pattern as a PDF file
3. Display the pattern in a matplotlib window

## Customization

You can modify the pattern parameters in each example:
- `pname`: Pattern name/size identifier
- `gender`: 'w' for women, 'm' for men
- `style`: Drafting style (Gilewska, Chiappetta, Donnanno)
- Additional parameters specific to each pattern type

Refer to the OpenPattern documentation for more options and customization possibilities.
