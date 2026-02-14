#!/usr/bin/env python3
"""
OpenPattern Interface - Sewing Pattern Generator

This script generates standard sewing patterns using OpenPattern library:
- Basic Bodice (Gilewska style)
- Basic Skirt (Chiappetta style)  
- Basic Trousers (Donnanno style)

All patterns are exported as PDF files.

Usage:
    # Generate all patterns
    python generate_patterns.py
    
    # Generate specific pattern type and size
    python generate_patterns.py --type bodice --size W36G
    
    # Generate pattern from bespoke measurements JSON file
    python generate_patterns.py --json test_measurements.json
"""

import os
import sys
import json
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for headless systems
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D

try:
    import OpenPattern as OP
except ImportError:
    print("Error: OpenPattern is not installed.")
    print("Please install it using:")
    print("  pip install git+https://github.com/fmetivier/OpenPattern.git")
    sys.exit(1)


def split_sleeve_into_pieces(sleeve_vertices, num_pieces=2):
    """
    Split a basic sleeve pattern into multiple pieces for better fit and shaping.
    
    Args:
        sleeve_vertices: List of [x, y] coordinates defining the sleeve outline
        num_pieces: Number of pieces to split into (2 or 3)
    
    Returns:
        List of piece definitions, each containing vertices and metadata
    """
    if not sleeve_vertices or len(sleeve_vertices) < 10:
        raise ValueError("Invalid sleeve vertices")
    
    vertices = np.array([[float(v[0]), float(v[1])] for v in sleeve_vertices])
    
    # Find the approximate center line of the sleeve (vertical split)
    x_coords = vertices[:, 0]
    y_coords = vertices[:, 1]
    
    # Find top (cap) and bottom (cuff) of sleeve
    top_y = y_coords.max()
    bottom_y = y_coords.min()
    sleeve_height = top_y - bottom_y
    
    if num_pieces == 2:
        return _create_two_piece_sleeve(vertices, top_y, bottom_y, sleeve_height)
    elif num_pieces == 3:
        return _create_three_piece_sleeve(vertices, top_y, bottom_y, sleeve_height)
    else:
        raise ValueError(f"Unsupported number of pieces: {num_pieces}. Must be 2 or 3.")


def _create_two_piece_sleeve(vertices, top_y, bottom_y, sleeve_height):
    """
    Create a two-piece sleeve following proper tailoring standards.
    
    In a proper two-piece sleeve:
    - Upper sleeve (oversleeve): covers the back/outer arm, wider at sleeve cap
    - Under sleeve (undersleeve): covers the front/inner arm, narrower at cap
    
    The split runs along the elbow line from back-center of cap through the 
    elbow to back-center of cuff, creating an anatomically correct division.
    """
    pieces = []
    
    # Analyze sleeve structure to find front and back edges
    # The sleeve vertices typically go around the perimeter
    # We need to identify which side is front (narrower at cap) and which is back (wider at cap)
    
    # Find the rightmost and leftmost edges at different heights
    # At the cap, back side is typically wider (further from center)
    cap_region = vertices[vertices[:, 1] >= (top_y - sleeve_height * 0.15)]
    mid_region = vertices[(vertices[:, 1] >= (bottom_y + sleeve_height * 0.4)) & 
                          (vertices[:, 1] <= (bottom_y + sleeve_height * 0.6))]
    cuff_region = vertices[vertices[:, 1] <= (bottom_y + sleeve_height * 0.15)]
    
    # Determine which side is front and which is back
    # Back side (right in standard orientation) is typically wider at cap
    if len(cap_region) > 0:
        right_cap_extent = np.max(cap_region[:, 0])
        left_cap_extent = np.min(cap_region[:, 0])
        # If right side extends further, it's the back
        back_is_right = abs(right_cap_extent) > abs(left_cap_extent)
    else:
        back_is_right = True  # Default assumption
    
    # Create split line that runs from back of cap through elbow to back of cuff
    # This split should be offset toward the back (typically 55-60% back, 40-45% front)
    split_points = []
    
    for height_ratio in np.linspace(1.0, 0, 25):
        y_level = bottom_y + sleeve_height * height_ratio
        
        # Find points at this height
        nearby_points = vertices[np.abs(vertices[:, 1] - y_level) < sleeve_height * 0.04]
        
        if len(nearby_points) > 0:
            x_min = np.min(nearby_points[:, 0])
            x_max = np.max(nearby_points[:, 0])
            
            # At cap: split closer to back edge (60% toward back)
            # At mid: split closer to center but still back-biased (55%)
            # At cuff: split at or near center (50%)
            if height_ratio > 0.7:  # Cap region
                back_bias = 0.60
            elif height_ratio > 0.3:  # Mid region (elbow)
                back_bias = 0.55
            else:  # Cuff region
                back_bias = 0.50
            
            if back_is_right:
                # Back is on the right, so split should be right of center
                split_x = x_min + (x_max - x_min) * back_bias
            else:
                # Back is on the left, so split should be left of center
                split_x = x_max - (x_max - x_min) * back_bias
            
            split_points.append([split_x, y_level])
    
    split_line = np.array(split_points)
    
    # Separate vertices into upper (back) and under (front) pieces
    # The upper sleeve should include the back portion (wider at cap)
    upper_vertices = []
    under_vertices = []
    
    for v in vertices:
        x, y = v
        # Find closest point on split line
        distances = np.sqrt((split_line[:, 0] - x)**2 + (split_line[:, 1] - y)**2)
        closest_idx = distances.argmin()
        split_x = split_line[closest_idx, 0]
        
        # Determine which piece this vertex belongs to
        if back_is_right:
            # Back (upper) is on the right side
            if x >= split_x:
                upper_vertices.append(v)
            else:
                under_vertices.append(v)
        else:
            # Back (upper) is on the left side
            if x <= split_x:
                upper_vertices.append(v)
            else:
                under_vertices.append(v)
    
    # Add split line to both pieces to create the seam
    if back_is_right:
        upper_vertices.extend(split_line[::-1])  # Add in reverse for proper polygon
        under_vertices.extend(split_line)
    else:
        upper_vertices.extend(split_line)
        under_vertices.extend(split_line[::-1])
    
    pieces.append({
        'name': 'Upper Sleeve (Oversleeve)',
        'vertices': np.array(upper_vertices),
        'description': 'Back/outer sleeve piece - wider at cap for back of arm'
    })
    
    pieces.append({
        'name': 'Under Sleeve (Undersleeve)',
        'vertices': np.array(under_vertices),
        'description': 'Front/inner sleeve piece - narrower at cap, wider at forearm'
    })
    
    return pieces


def _create_three_piece_sleeve(vertices, top_y, bottom_y, sleeve_height):
    """
    Create a three-piece sleeve: upper sleeve, under sleeve, and cuff piece.
    This style is used in Chanel jackets and allows for better wrist shaping.
    """
    pieces = []
    
    # First split into upper and under like the two-piece
    two_piece = _create_two_piece_sleeve(vertices, top_y, bottom_y, sleeve_height)
    
    # Now split the lower portion (cuff area) from both pieces
    # The cuff typically occupies the lower 20-25% of the sleeve
    cuff_split_y = bottom_y + sleeve_height * 0.25
    
    for i, piece in enumerate(two_piece):
        piece_vertices = piece['vertices']
        
        # Split this piece at the cuff line
        upper_part = []
        cuff_part = []
        transition_points = []
        
        for v in piece_vertices:
            if v[1] > cuff_split_y:
                upper_part.append(v)
            elif abs(v[1] - cuff_split_y) < sleeve_height * 0.02:
                # Points near the split line go to both
                transition_points.append(v)
            else:
                cuff_part.append(v)
        
        # Add transition points to both parts
        upper_part.extend(transition_points)
        cuff_part.extend(transition_points[::-1])
        
        if i == 0:  # Upper sleeve
            pieces.append({
                'name': 'Upper Sleeve (Back)',
                'vertices': np.array(upper_part),
                'description': 'Upper/back sleeve piece (top portion)'
            })
        else:  # Under sleeve
            pieces.append({
                'name': 'Under Sleeve (Front)',
                'vertices': np.array(upper_part),
                'description': 'Under/front sleeve piece (top portion)'
            })
    
    # Combine cuff parts from both pieces into one cuff piece
    # The cuff wraps around the wrist
    all_cuff_points = []
    for piece in two_piece:
        piece_vertices = piece['vertices']
        cuff_points = [v for v in piece_vertices if v[1] <= cuff_split_y + sleeve_height * 0.02]
        all_cuff_points.extend(cuff_points)
    
    if all_cuff_points:
        pieces.append({
            'name': 'Cuff Piece',
            'vertices': np.array(all_cuff_points),
            'description': 'Cuff piece for wrist shaping (Chanel-style)'
        })
    
    return pieces


def draw_multi_piece_sleeve(pieces, title="Multi-Piece Sleeve Pattern"):
    """
    Draw multiple sleeve pieces on a single figure for visualization.
    
    Args:
        pieces: List of piece dictionaries with 'name', 'vertices', and 'description'
        title: Title for the plot
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    for i, piece in enumerate(pieces):
        vertices = piece['vertices']
        if len(vertices) > 0:
            color = colors[i % len(colors)]
            
            # Draw the piece outline
            poly = Polygon(vertices, fill=False, edgecolor=color, 
                          linewidth=2, linestyle='-', label=piece['name'])
            ax.add_patch(poly)
            
            # Add piece label at the centroid
            centroid = vertices.mean(axis=0)
            ax.text(centroid[0], centroid[1], piece['name'], 
                   fontsize=10, ha='center', va='center',
                   bbox=dict(boxstyle='round', facecolor=color, alpha=0.3))
            
            # Add notches/marks at key points
            if len(vertices) > 0:
                # Mark the first point
                ax.plot(vertices[0, 0], vertices[0, 1], 'ko', markersize=6)
    
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel('Width (cm)', fontsize=10)
    ax.set_ylabel('Length (cm)', fontsize=10)
    
    return fig, ax


def generate_bodice(pname="W36G", gender='w', style='Gilewska', output_dir='output', 
                   with_sleeves=False, sleeve_style=None, sleeve_pieces=1):
    """
    Generate a basic bodice pattern.
    
    Args:
        pname: Pattern name (e.g., W36G = Women's size 36, Gilewska style)
        gender: 'w' for women, 'm' for men
        style: Pattern drafting style (e.g., 'Gilewska', 'Chiappetta')
        output_dir: Directory to save the PDF
        with_sleeves: Whether to add sleeves to the bodice
        sleeve_style: Sleeve style ('Gilewska', 'Chiappetta'), defaults to bodice style
        sleeve_pieces: Number of pieces for sleeve (1=basic, 2=two-piece, 3=three-piece)
    """
    print(f"\nGenerating bodice pattern: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    if with_sleeves:
        print(f"  With sleeves: {sleeve_style or style}")
        if sleeve_pieces > 1:
            print(f"  Sleeve pieces: {sleeve_pieces}")
    
    # Create the bodice pattern
    p = OP.Basic_Bodice(
        pname=pname,
        gender=gender,
        style=style
    )
    
    # Add sleeves if requested
    if with_sleeves:
        add_sleeves_to_bodice(p, gender, sleeve_style or style)
    
    # Save as PDF
    os.makedirs(output_dir, exist_ok=True)
    sleeve_suffix = '_with_sleeves' if with_sleeves else ''
    if sleeve_pieces > 1:
        sleeve_suffix += f'_{sleeve_pieces}piece'
    pdf_path = os.path.join(output_dir, f'bodice_{pname}{sleeve_suffix}.pdf')
    
    if with_sleeves:
        # Save multi-page PDF with bodice and sleeves
        with PdfPages(pdf_path) as pdf:
            # Page 1: Bodice
            p.draw_bodice()
            pdf.savefig(plt.gcf(), bbox_inches='tight')
            plt.close()
            
            if sleeve_pieces == 1:
                # Page 2: Basic single-piece sleeves
                p.draw_sleeves(save=False)
                pdf.savefig(plt.gcf(), bbox_inches='tight')
                plt.close()
                print(f"  Saved: {pdf_path} (bodice on page 1, sleeves on page 2)")
            else:
                # Page 2: Original sleeve pattern for reference
                p.draw_sleeves(save=False)
                plt.title('Original Single-Piece Sleeve (Reference)', fontsize=12)
                pdf.savefig(plt.gcf(), bbox_inches='tight')
                plt.close()
                
                # Page 3+: Multi-piece sleeve patterns
                try:
                    sleeve_vertices = p.Sleeve_vertices
                    pieces = split_sleeve_into_pieces(sleeve_vertices, num_pieces=sleeve_pieces)
                    
                    # Draw all pieces together for overview
                    fig, ax = draw_multi_piece_sleeve(
                        pieces, 
                        title=f'{sleeve_pieces}-Piece Sleeve Pattern Overview'
                    )
                    pdf.savefig(fig, bbox_inches='tight')
                    plt.close()
                    
                    # Draw each piece separately for printing
                    for i, piece in enumerate(pieces, 1):
                        fig, ax = plt.subplots(figsize=(10, 12))
                        vertices = piece['vertices']
                        
                        if len(vertices) > 0:
                            poly = Polygon(vertices, fill=False, edgecolor='black', 
                                         linewidth=2, linestyle='-')
                            ax.add_patch(poly)
                            
                            # Add notches at key points
                            ax.plot(vertices[0, 0], vertices[0, 1], 'ko', markersize=8, 
                                   label='Start point')
                            
                            # Add grainline indicator
                            centroid = vertices.mean(axis=0)
                            y_range = vertices[:, 1].max() - vertices[:, 1].min()
                            grain_start = [centroid[0], centroid[1] - y_range * 0.3]
                            grain_end = [centroid[0], centroid[1] + y_range * 0.3]
                            ax.arrow(grain_start[0], grain_start[1], 
                                   0, grain_end[1] - grain_start[1],
                                   head_width=0.5, head_length=1, fc='blue', ec='blue',
                                   label='Grainline')
                        
                        ax.set_aspect('equal')
                        ax.grid(True, alpha=0.3)
                        ax.legend(loc='upper right')
                        ax.set_title(f'{piece["name"]}\n{piece["description"]}', 
                                   fontsize=14, fontweight='bold')
                        ax.set_xlabel('Width (cm)', fontsize=10)
                        ax.set_ylabel('Length (cm)', fontsize=10)
                        
                        pdf.savefig(fig, bbox_inches='tight')
                        plt.close()
                    
                    print(f"  Saved: {pdf_path} ({sleeve_pieces}-piece sleeve with {len(pieces)} pattern pieces)")
                    
                except Exception as e:
                    print(f"  Warning: Could not create multi-piece sleeve: {e}")
                    print(f"  Saved basic sleeve pattern instead")
    else:
        # Draw and save just the bodice
        p.draw()
        plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
        print(f"  Saved: {pdf_path}")
        plt.close()
    
    return pdf_path


def add_sleeves_to_bodice(bodice, gender, sleeve_style='Gilewska'):
    """
    Add sleeves to an existing bodice pattern.
    
    This function transforms a basic bodice by adding sleeves according to
    the specified style. The sleeve is automatically fitted to the armhole
    of the bodice.
    
    Args:
        bodice: OP.Basic_Bodice instance
        gender: 'w' for women, 'm' for men
        sleeve_style: Style of sleeve ('Gilewska', 'Chiappetta')
    
    Returns:
        The modified bodice with sleeves added
    
    Note:
        Some sleeve styles may only work with specific bodice styles or genders.
        If a sleeve method is not compatible, it will fall back to Gilewska style.
        
        Chiappetta sleeves for women use the men's method as a fallback since
        OpenPattern's chiappetta_basic_sleeve_m works for both genders.
    """
    print(f"  Adding {sleeve_style} sleeves...")
    
    # Map of sleeve methods for each style and gender
    # Note: Not all combinations are available in OpenPattern
    sleeve_methods = {
        ('Gilewska', 'w'): 'Gilewska_basic_sleeve_w',
        ('Gilewska', 'm'): 'Gilewska_basic_sleeve_m',
        ('Chiappetta', 'm'): 'chiappetta_armhole_sleeve_m',
        ('Chiappetta', 'w'): 'chiappetta_basic_sleeve_m',  # Uses men's method (works for both)
    }
    
    # Get the appropriate sleeve method
    method_name = sleeve_methods.get((sleeve_style, gender))
    
    if not method_name:
        print(f"  Warning: {sleeve_style} sleeves not available for gender '{gender}', using Gilewska")
        method_name = sleeve_methods.get(('Gilewska', gender))
    
    if hasattr(bodice, method_name):
        try:
            method = getattr(bodice, method_name)
            method()
            print(f"  Sleeves added successfully using {method_name}")
        except Exception as e:
            print(f"  Warning: Failed to add {sleeve_style} sleeves: {e}")
            # Try fallback to Gilewska
            if sleeve_style != 'Gilewska':
                print(f"  Trying Gilewska sleeves as fallback...")
                fallback_method = sleeve_methods.get(('Gilewska', gender))
                if fallback_method and hasattr(bodice, fallback_method):
                    try:
                        method = getattr(bodice, fallback_method)
                        method()
                        print(f"  Sleeves added using fallback: {fallback_method}")
                    except Exception as e2:
                        print(f"  Error: Could not add sleeves: {e2}")
    else:
        print(f"  Warning: Method {method_name} not found on bodice")
    
    return bodice


def generate_skirt(pname="W6C", gender='G', style='Chiappetta', ease=8, curves=False, output_dir='output'):
    """
    Generate a basic skirt pattern.
    
    Args:
        pname: Pattern name (e.g., W6C = Women's size, Chiappetta style)
        gender: Gender code - Note: OpenPattern's Basic_Skirt requires 'G' (not 'w' or 'm')
               This is an OpenPattern API requirement, not a standard gender code
        style: Pattern drafting style (e.g., 'Chiappetta')
        ease: Ease in cm
        curves: Whether to use curves
        output_dir: Directory to save the PDF
    """
    print(f"\nGenerating skirt pattern: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    print(f"  Ease: {ease} cm")
    
    # Create the skirt pattern
    # Note: OpenPattern's Basic_Skirt uses different parameters than Basic_Bodice/Basic_Trousers
    p = OP.Basic_Skirt(
        pname=pname,
        style=style,
        gender=gender,  # OpenPattern requires 'G' for skirts
        ease=ease,
        curves=curves
    )
    
    # Draw the pattern
    p.draw()
    
    # Save as PDF
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, f'skirt_{pname}.pdf')
    plt.savefig(pdf_path, format='pdf', bbox_inches='tight')
    print(f"  Saved: {pdf_path}")
    
    plt.close()
    return pdf_path


def generate_trousers(pname="M44D", gender='m', style='Donnanno', darts=True, output_dir='output'):
    """
    Generate a basic trousers pattern.
    
    Args:
        pname: Pattern name (e.g., M44D = Men's size 44, Donnanno style)
        gender: 'w' for women, 'm' for men
        style: Pattern drafting style (e.g., 'Donnanno')
        darts: Whether to include darts
        output_dir: Directory to save the PDF
    """
    print(f"\nGenerating trousers pattern: {pname}")
    print(f"  Gender: {gender}")
    print(f"  Style: {style}")
    print(f"  Darts: {darts}")
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the trousers pattern
    trousers = OP.Basic_Trousers(
        pname=pname,
        gender=gender,
        style=style,
        darts=darts,
        figPATH=output_dir + "/",
        frmt="pdf",
    )
    
    # Draw the pattern
    trousers.draw_basic_trousers(
        dic={"Pattern": "Basic trousers with dart"}, 
        save=True
    )
    
    pdf_path = os.path.join(output_dir, f'{pname}_basic_trousers.pdf')
    print(f"  Saved: {pdf_path}")
    
    plt.close()
    return pdf_path


def load_measurements_from_json(json_file):
    """
    Load bespoke measurements from a JSON file.
    
    Args:
        json_file: Path to JSON file containing measurements
        
    Returns:
        Dictionary with pattern parameters
    """
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        pattern_type = data.get('type', '')
        if not pattern_type:
            raise ValueError("Missing required field 'type' in JSON file")
        
        pattern_type = pattern_type.lower()
        if pattern_type not in ['bodice', 'skirt', 'trousers']:
            raise ValueError(f"Invalid pattern type: '{pattern_type}'. Must be 'bodice', 'skirt', or 'trousers'")
        
        return data
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{json_file}': {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)


def ensure_pattern_suffix(name, pattern_type):
    """
    Ensure the pattern name has the correct suffix based on pattern type.
    
    OpenPattern uses specific suffix conventions to identify pattern styles:
    - 'G' for Gilewska style (typically bodice patterns)
    - 'C' for Chiappetta style (typically skirt patterns)
    - 'D' for Donnanno style (typically trousers patterns)
    
    Args:
        name: Pattern name (e.g., 'W36', 'W8', 'M44')
        pattern_type: Type of pattern ('bodice', 'skirt', or 'trousers')
        
    Returns:
        Pattern name with correct suffix (e.g., 'W36G', 'W8C', 'M44D')
    """
    suffix_map = {
        'bodice': 'G',
        'skirt': 'C',
        'trousers': 'D'
    }
    
    suffix = suffix_map.get(pattern_type)
    if suffix and not name.endswith(suffix):
        return f"{name}{suffix}"
    return name


def generate_from_json(json_file, output_dir='output'):
    """
    Generate a pattern from bespoke measurements in a JSON file.
    
    Args:
        json_file: Path to JSON file containing measurements and parameters
        output_dir: Directory to save the PDF
    """
    print(f"\nLoading measurements from: {json_file}")
    data = load_measurements_from_json(json_file)
    
    pattern_type = data['type'].lower()
    name = data.get('name', 'custom')
    style = data.get('style', 'Gilewska')
    gender = data.get('gender', 'w')
    
    print(f"Pattern type: {pattern_type}")
    print(f"Pattern name: {name}")
    
    # Check for transformations
    transformations = data.get('transformations', {})
    
    # Generate the appropriate pattern type
    # Note: OpenPattern uses standard sizes, but we can still pass the name
    if pattern_type == 'bodice':
        pname = ensure_pattern_suffix(name, 'bodice')
        
        # Check for sleeve transformation
        with_sleeves = transformations.get('add_sleeves', False)
        sleeve_style = transformations.get('sleeve_style', style)
        sleeve_pieces = transformations.get('sleeve_pieces', 1)
        
        pdf_path = generate_bodice(
            pname=pname,
            gender=gender,
            style=style,
            output_dir=output_dir,
            with_sleeves=with_sleeves,
            sleeve_style=sleeve_style,
            sleeve_pieces=sleeve_pieces
        )
    elif pattern_type == 'skirt':
        pname = ensure_pattern_suffix(name, 'skirt')
        ease = data.get('ease', 8)
        curves = data.get('curves', False)
        pdf_path = generate_skirt(
            pname=pname,
            gender=gender,
            style=style,
            ease=ease,
            curves=curves,
            output_dir=output_dir
        )
    elif pattern_type == 'trousers':
        pname = ensure_pattern_suffix(name, 'trousers')
        darts = data.get('darts', True)
        pdf_path = generate_trousers(
            pname=pname,
            gender=gender,
            style=style,
            darts=darts,
            output_dir=output_dir
        )
    
    return pdf_path


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate sewing patterns using OpenPattern library',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all default patterns
  python generate_patterns.py
  
  # Generate a specific bodice pattern
  python generate_patterns.py --type bodice --size W36G
  
  # Generate a bodice with sleeves
  python generate_patterns.py --type bodice --size W36G --add-sleeves
  
  # Generate a skirt pattern
  python generate_patterns.py --type skirt --size W6C
  
  # Generate from custom measurements JSON
  python generate_patterns.py --json test_measurements.json
        """
    )
    
    parser.add_argument(
        '--type',
        choices=['bodice', 'skirt', 'trousers'],
        help='Pattern type to generate'
    )
    
    parser.add_argument(
        '--size',
        help='Pattern size (e.g., W36G for bodice, W6C for skirt, M44D for trousers)'
    )
    
    parser.add_argument(
        '--json',
        help='Path to JSON file with bespoke measurements'
    )
    
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory for PDF files (default: output)'
    )
    
    parser.add_argument(
        '--style',
        help='Pattern drafting style (e.g., Gilewska, Chiappetta, Donnanno)'
    )
    
    parser.add_argument(
        '--gender',
        choices=['w', 'm', 'G'],
        help='Gender code: w=women, m=men, G=general (for skirts)'
    )
    
    parser.add_argument(
        '--add-sleeves',
        action='store_true',
        help='Add sleeves to bodice pattern (only for bodice type)'
    )
    
    parser.add_argument(
        '--sleeve-style',
        choices=['Gilewska', 'Chiappetta'],
        help='Sleeve style (defaults to bodice style)'
    )
    
    parser.add_argument(
        '--sleeve-pieces',
        type=int,
        choices=[1, 2, 3],
        default=1,
        help='Number of pieces for sleeve: 1=basic (default), 2=two-piece for better fit, 3=three-piece Chanel-style'
    )
    
    return parser.parse_args()


def main():
    """Main function to generate patterns based on arguments."""
    args = parse_arguments()
    
    print("=" * 60)
    print("OpenPattern Interface - Sewing Pattern Generator")
    print("=" * 60)
    
    output_dir = args.output
    
    # Generate from JSON file if provided
    if args.json:
        generate_from_json(args.json, output_dir)
        print("\n" + "=" * 60)
        print("Pattern generation complete!")
        print(f"Pattern saved to '{output_dir}/' directory")
        print("=" * 60)
        return
    
    # Generate specific pattern type if specified
    if args.type:
        if not args.size:
            # Provide helpful error message with examples based on pattern type
            size_examples = {
                'bodice': 'W36G, W38G, W40G, M44G',
                'skirt': 'W6C, W8C, W10C',
                'trousers': 'M44D, M46D, W38D'
            }
            examples = size_examples.get(args.type, 'W36G, W6C, M44D')
            print(f"Error: --size is required when --type is specified")
            print(f"Example sizes for {args.type}: {examples}")
            sys.exit(1)
        
        pattern_type = args.type.lower()
        size = args.size
        
        # Extract style from size or use provided style
        if pattern_type == 'bodice':
            style = args.style or 'Gilewska'
            gender = args.gender or 'w'
            
            # Check for sleeve transformation
            with_sleeves = args.add_sleeves
            sleeve_style = args.sleeve_style or style
            sleeve_pieces = args.sleeve_pieces
            
            # Warn if sleeve options used without bodice
            if with_sleeves and pattern_type != 'bodice':
                print("Warning: --add-sleeves only applies to bodice patterns")
                with_sleeves = False
            
            generate_bodice(
                pname=size,
                gender=gender,
                style=style,
                output_dir=output_dir,
                with_sleeves=with_sleeves,
                sleeve_style=sleeve_style,
                sleeve_pieces=sleeve_pieces
            )
        elif pattern_type == 'skirt':
            style = args.style or 'Chiappetta'
            gender = args.gender or 'G'
            generate_skirt(
                pname=size,
                gender=gender,
                style=style,
                ease=8,
                curves=False,
                output_dir=output_dir
            )
        elif pattern_type == 'trousers':
            style = args.style or 'Donnanno'
            gender = args.gender or 'm'
            generate_trousers(
                pname=size,
                gender=gender,
                style=style,
                darts=True,
                output_dir=output_dir
            )
        
        print("\n" + "=" * 60)
        print("Pattern generation complete!")
        print(f"Pattern saved to '{output_dir}/' directory")
        print("=" * 60)
        return
    
    # Default: Generate all pattern types
    bodice_pdf = generate_bodice(
        pname="W36G",
        gender='w',
        style='Gilewska',
        output_dir=output_dir
    )
    
    skirt_pdf = generate_skirt(
        pname="W6C",
        gender='G',
        style='Chiappetta',
        ease=8,
        curves=False,
        output_dir=output_dir
    )
    
    trousers_pdf = generate_trousers(
        pname="M44D",
        gender='m',
        style='Donnanno',
        darts=True,
        output_dir=output_dir
    )
    
    print("\n" + "=" * 60)
    print("Pattern generation complete!")
    print(f"All patterns saved to '{output_dir}/' directory")
    print("=" * 60)


if __name__ == "__main__":
    main()
