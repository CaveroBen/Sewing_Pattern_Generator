"""
Export functionality for sewing patterns.
Handles PDF generation (full-size and tiled A4) and JPG thumbnail creation with
proper pattern layout, markings, and annotations.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import os
import math


class PatternExporter:
    """
    Class for exporting patterns to PDF and JPG formats with professional markings.
    """
    
    # A4 dimensions in cm
    A4_WIDTH = 21.0
    A4_HEIGHT = 29.7
    
    # Margins in cm
    MARGIN = 2.0
    PIECE_SPACING = 5.0  # Space between pattern pieces
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize exporter.
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def _extract_points(self, piece_data) -> List[Tuple[float, float]]:
        """
        Extract points from pattern piece data (handles both old and new format).
        
        Args:
            piece_data: Either a list of points or a dict with 'points' key
            
        Returns:
            List of (x, y) tuples
        """
        if isinstance(piece_data, dict):
            return piece_data.get('points', [])
        return piece_data
    
    def _get_piece_metadata(self, piece_data) -> Dict[str, Any]:
        """
        Get metadata from pattern piece data.
        
        Args:
            piece_data: Pattern piece data (dict or list)
            
        Returns:
            Dictionary with metadata (label, cutting, grainline, notches)
        """
        if isinstance(piece_data, dict):
            return {
                'label': piece_data.get('label', ''),
                'cutting': piece_data.get('cutting', ''),
                'grainline': piece_data.get('grainline', 'vertical'),
                'notches': piece_data.get('notches', [])
            }
        return {
            'label': '',
            'cutting': '',
            'grainline': 'vertical',
            'notches': []
        }
    
    def _layout_pieces(self, pattern_pieces: dict) -> Dict[str, Tuple[float, float]]:
        """
        Calculate optimal layout positions for pattern pieces to avoid overlap.
        
        Args:
            pattern_pieces: Dictionary of pattern pieces
            
        Returns:
            Dictionary mapping piece names to (offset_x, offset_y) tuples
        """
        offsets = {}
        current_x = 0
        current_y = 0
        max_height_in_row = 0
        max_total_width = 0
        
        for piece_name, piece_data in pattern_pieces.items():
            points = self._extract_points(piece_data)
            if not points:
                continue
            
            # Calculate piece dimensions
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            piece_width = max(xs) - min(xs)
            piece_height = max(ys) - min(ys)
            
            # Position this piece
            offsets[piece_name] = (current_x - min(xs), current_y - min(ys))
            
            # Update position for next piece (arrange in rows)
            current_x += piece_width + self.PIECE_SPACING
            max_height_in_row = max(max_height_in_row, piece_height)
            max_total_width = max(max_total_width, current_x)
            
            # Start new row if we've placed multiple pieces
            if len(offsets) % 3 == 0:  # 3 pieces per row
                current_x = 0
                current_y += max_height_in_row + self.PIECE_SPACING
                max_height_in_row = 0
        
        return offsets
    
    def export_pattern(self, pattern_pieces: dict, garment_type: str,
                      title: str, full_pdf: bool = True, 
                      tiled_pdf: bool = False, jpg: bool = True) -> dict:
        """
        Export pattern pieces to various formats.
        Supports both OpenPattern objects and legacy point-based patterns.
        
        Args:
            pattern_pieces: Dictionary containing either OpenPattern objects or point lists
            garment_type: Type of garment (shirt, vest, etc.)
            title: Title for the pattern
            full_pdf: Generate full-size PDF
            tiled_pdf: Generate A4-tiled PDF
            jpg: Generate JPG thumbnail
            
        Returns:
            Dictionary of generated file paths
        """
        output_files = {}
        
        # Check if this is an OpenPattern object
        if self._is_openpattern_object(pattern_pieces):
            return self._export_openpattern(pattern_pieces, garment_type, title, full_pdf, tiled_pdf, jpg)
        
        # Legacy export for point-based patterns
        # Generate full-size PDF
        if full_pdf:
            pdf_path = os.path.join(self.output_dir, f"{garment_type}_pattern.pdf")
            self._create_full_pdf(pattern_pieces, title, pdf_path)
            output_files["pdf"] = pdf_path
        
        # Generate tiled A4 PDF
        if tiled_pdf:
            tiled_path = os.path.join(self.output_dir, f"{garment_type}_pattern_tiled.pdf")
            self._create_tiled_pdf(pattern_pieces, title, tiled_path)
            output_files["tiled_pdf"] = tiled_path
        
        # Generate JPG thumbnail
        if jpg:
            jpg_path = os.path.join(self.output_dir, f"{garment_type}_pattern.jpg")
            self._create_jpg(pattern_pieces, title, jpg_path)
            output_files["jpg"] = jpg_path
        
        return output_files
    
    def _is_openpattern_object(self, pattern_pieces: dict) -> bool:
        """
        Check if pattern_pieces contains an OpenPattern object.
        
        Args:
            pattern_pieces: Pattern data dictionary
            
        Returns:
            True if this is an OpenPattern object, False otherwise
        """
        return (isinstance(pattern_pieces, dict) and 
                pattern_pieces.get('type') == 'openpattern' and
                'openpattern_object' in pattern_pieces)
    
    def _export_openpattern(self, pattern_data: dict, garment_type: str,
                          title: str, full_pdf: bool = True,
                          tiled_pdf: bool = False, jpg: bool = True) -> dict:
        """
        Export OpenPattern object to PDF and JPG using OpenPattern's native methods.
        
        Args:
            pattern_data: Dictionary containing OpenPattern object
            garment_type: Type of garment
            title: Pattern title
            full_pdf: Generate full-size PDF
            tiled_pdf: Generate A4-tiled PDF  
            jpg: Generate JPG thumbnail
            
        Returns:
            Dictionary of generated file paths
        """
        import matplotlib.pyplot as plt
        
        output_files = {}
        pattern_obj = pattern_data['openpattern_object']
        
        # Generate full-size PDF using OpenPattern's draw method
        if full_pdf:
            pdf_path = os.path.join(self.output_dir, f"{garment_type}_pattern.pdf")
            
            # Create figure and draw pattern
            fig = plt.figure(figsize=(11, 17), dpi=100)  # A3 size in inches at 100dpi
            pattern_obj.draw()
            
            # Add title
            plt.suptitle(title, fontsize=16, fontweight='bold')
            
            # Save to PDF
            plt.savefig(pdf_path, format='pdf', bbox_inches='tight', dpi=100)
            plt.close(fig)
            
            output_files["pdf"] = pdf_path
        
        # Generate JPG thumbnail
        if jpg:
            jpg_path = os.path.join(self.output_dir, f"{garment_type}_pattern.jpg")
            
            # Create figure and draw pattern
            fig = plt.figure(figsize=(11, 17), dpi=100)
            pattern_obj.draw()
            
            # Add title
            plt.suptitle(title, fontsize=16, fontweight='bold')
            
            # Save to JPG (use 'jpeg' format for compatibility)
            plt.savefig(jpg_path, format='jpeg', bbox_inches='tight', dpi=100)
            plt.close(fig)
            
            output_files["jpg"] = jpg_path
        
        # Generate tiled PDF
        # Note: Full tiling of OpenPattern objects is complex and not yet implemented.
        # This creates a standard PDF that can be printed and manually tiled.
        if tiled_pdf:
            tiled_path = os.path.join(self.output_dir, f"{garment_type}_pattern_tiled.pdf")
            
            fig = plt.figure(figsize=(11, 17), dpi=100)
            pattern_obj.draw()
            plt.suptitle(f"{title} (For Tiling)", fontsize=16, fontweight='bold')
            
            # Add note about manual tiling
            fig.text(0.5, 0.02, 
                    'Note: This PDF can be printed and manually tiled. '
                    'Automatic A4 tiling not yet supported for OpenPattern objects.',
                    ha='center', fontsize=8, style='italic', wrap=True)
            
            plt.savefig(tiled_path, format='pdf', bbox_inches='tight', dpi=100)
            plt.close(fig)
            
            output_files["tiled_pdf"] = tiled_path
        
        return output_files
    
    def _create_full_pdf(self, pattern_pieces: dict, title: str, output_path: str):
        """Create a full-size PDF of the pattern with proper layout and markings."""
        # Calculate layout positions
        offsets = self._layout_pieces(pattern_pieces)
        
        # Calculate overall dimensions after layout
        all_points = []
        for piece_name, piece_data in pattern_pieces.items():
            points = self._extract_points(piece_data)
            if not points or piece_name not in offsets:
                continue
            offset_x, offset_y = offsets[piece_name]
            for x, y in points:
                all_points.append((x + offset_x, y + offset_y))
        
        if not all_points:
            return
        
        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        width = max_x - min_x + 4 * self.MARGIN
        height = max_y - min_y + 4 * self.MARGIN
        
        # Create figure with size in inches (convert from cm)
        fig = plt.figure(figsize=(width / 2.54, height / 2.54), dpi=100)
        ax = fig.add_subplot(111)
        
        # Set up coordinate system (1:1 scale in cm)
        ax.set_xlim(min_x - 2*self.MARGIN, max_x + 2*self.MARGIN)
        ax.set_ylim(min_y - 2*self.MARGIN, max_y + 2*self.MARGIN)
        ax.set_aspect('equal')
        
        # Draw pattern pieces with proper layout
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        for i, (piece_name, piece_data) in enumerate(pattern_pieces.items()):
            points = self._extract_points(piece_data)
            metadata = self._get_piece_metadata(piece_data)
            
            if not points or piece_name not in offsets:
                continue
            
            offset_x, offset_y = offsets[piece_name]
            
            # Apply offset to points
            xs = [p[0] + offset_x for p in points]
            ys = [p[1] + offset_y for p in points]
            
            color = colors[i % len(colors)]
            
            # Draw pattern outline
            ax.plot(xs, ys, color=color, linewidth=2.5, label=piece_name, zorder=2)
            ax.fill(xs, ys, alpha=0.08, color=color, zorder=1)
            
            # Add pattern piece label
            center_x = sum(xs) / len(xs)
            center_y = sum(ys) / len(ys)
            if metadata['label']:
                ax.text(center_x, center_y + 3, metadata['label'], 
                       ha='center', va='center', fontsize=12, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))
            if metadata['cutting']:
                ax.text(center_x, center_y - 3, metadata['cutting'],
                       ha='center', va='center', fontsize=10, style='italic',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
            
            # Draw grainline arrow
            if metadata['grainline']:
                piece_min_y = min(ys)
                piece_max_y = max(ys)
                piece_min_x = min(xs)
                arrow_x = piece_min_x + (max(xs) - piece_min_x) * 0.15
                arrow_start_y = piece_min_y + (piece_max_y - piece_min_y) * 0.2
                arrow_end_y = piece_min_y + (piece_max_y - piece_min_y) * 0.8
                
                if metadata['grainline'] == 'vertical':
                    arrow = FancyArrowPatch(
                        (arrow_x, arrow_start_y), (arrow_x, arrow_end_y),
                        arrowstyle='<->', mutation_scale=20, linewidth=1.5,
                        color='black', zorder=3
                    )
                    ax.add_patch(arrow)
                    ax.text(arrow_x + 1, (arrow_start_y + arrow_end_y)/2, 'GRAIN',
                           rotation=90, va='center', fontsize=8)
        
        # Add 5cm grid (lighter than before)
        ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.2, color='gray')
        
        # Add major grid at 10cm intervals
        x_major = np.arange(math.floor(min_x / 10) * 10, math.ceil(max_x / 10) * 10 + 10, 10)
        y_major = np.arange(math.floor(min_y / 10) * 10, math.ceil(max_y / 10) * 10 + 10, 10)
        ax.set_xticks(x_major, minor=False)
        ax.set_yticks(y_major, minor=False)
        ax.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.3, color='gray')
        
        ax.set_xlabel('Width (cm)', fontsize=10, fontweight='bold')
        ax.set_ylabel('Length (cm)', fontsize=10, fontweight='bold')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        
        # Add pattern info box
        info_text = "1:1 SCALE - Print at 100%\nSeam allowance NOT included\nAdd 1.5cm seam allowance when cutting"
        ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
               fontsize=9, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # Add scale reference (10cm line)
        scale_x = min_x + self.MARGIN
        scale_y = min_y + self.MARGIN * 0.5
        ax.plot([scale_x, scale_x + 10], [scale_y, scale_y], 'k-', linewidth=4, zorder=5)
        ax.plot([scale_x, scale_x], [scale_y - 0.5, scale_y + 0.5], 'k-', linewidth=2, zorder=5)
        ax.plot([scale_x + 10, scale_x + 10], [scale_y - 0.5, scale_y + 0.5], 'k-', linewidth=2, zorder=5)
        ax.text(scale_x + 5, scale_y - 1.5, '10 cm SCALE', ha='center', 
               fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        # Save to PDF
        plt.tight_layout()
        plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=100)
        plt.close(fig)
    
    def _create_tiled_pdf(self, pattern_pieces: dict, title: str, output_path: str):
        """Create a tiled PDF for printing on A4 sheets with proper layout."""
        # Calculate layout positions
        offsets = self._layout_pieces(pattern_pieces)
        
        # Calculate overall dimensions after layout
        all_points = []
        for piece_name, piece_data in pattern_pieces.items():
            points = self._extract_points(piece_data)
            if not points or piece_name not in offsets:
                continue
            offset_x, offset_y = offsets[piece_name]
            for x, y in points:
                all_points.append((x + offset_x, y + offset_y))
        
        if not all_points:
            return
        
        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        total_width = max_x - min_x
        total_height = max_y - min_y
        
        # Calculate number of tiles needed
        usable_width = self.A4_WIDTH - 2 * self.MARGIN
        usable_height = self.A4_HEIGHT - 2 * self.MARGIN
        
        tiles_x = math.ceil(total_width / usable_width)
        tiles_y = math.ceil(total_height / usable_height)
        
        # Create multi-page PDF
        with PdfPages(output_path) as pdf:
            for tile_y in range(tiles_y):
                for tile_x in range(tiles_x):
                    # Calculate tile boundaries
                    tile_min_x = min_x + tile_x * usable_width
                    tile_max_x = min(tile_min_x + usable_width, max_x)
                    tile_min_y = min_y + tile_y * usable_height
                    tile_max_y = min(tile_min_y + usable_height, max_y)
                    
                    # Create A4 page
                    fig = plt.figure(figsize=(self.A4_WIDTH / 2.54, self.A4_HEIGHT / 2.54), dpi=100)
                    ax = fig.add_subplot(111)
                    
                    # Set coordinate system for this tile
                    ax.set_xlim(tile_min_x - self.MARGIN, tile_max_x + self.MARGIN)
                    ax.set_ylim(tile_min_y - self.MARGIN, tile_max_y + self.MARGIN)
                    ax.set_aspect('equal')
                    
                    # Draw pattern pieces (only parts visible in this tile)
                    colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
                    for i, (piece_name, piece_data) in enumerate(pattern_pieces.items()):
                        points = self._extract_points(piece_data)
                        if not points or piece_name not in offsets:
                            continue
                        
                        offset_x, offset_y = offsets[piece_name]
                        xs = [p[0] + offset_x for p in points]
                        ys = [p[1] + offset_y for p in points]
                        color = colors[i % len(colors)]
                        ax.plot(xs, ys, color=color, linewidth=2)
                        ax.fill(xs, ys, alpha=0.08, color=color)
                    
                    # Add grid
                    ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.2)
                    ax.set_xlabel('Width (cm)', fontsize=8)
                    ax.set_ylabel('Length (cm)', fontsize=8)
                    
                    # Add tile information
                    tile_title = f"{title} - Page {tile_x + tile_y * tiles_x + 1} of {tiles_x * tiles_y}"
                    ax.set_title(tile_title, fontsize=11)
                    
                    # Add alignment marks at corners
                    for corner_x in [tile_min_x, tile_max_x]:
                        for corner_y in [tile_min_y, tile_max_y]:
                            ax.plot(corner_x, corner_y, 'k+', markersize=12, markeredgewidth=2.5)
                    
                    # Add tile position info
                    info_text = f"Tile ({tile_x + 1}, {tile_y + 1})\nof ({tiles_x}, {tiles_y})"
                    ax.text(0.98, 0.02, info_text, transform=ax.transAxes,
                           fontsize=8, verticalalignment='bottom', horizontalalignment='right',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
                    
                    pdf.savefig(fig, bbox_inches='tight', dpi=100)
                    plt.close(fig)
    
    def _create_jpg(self, pattern_pieces: dict, title: str, output_path: str, max_size: int = 1200):
        """Create a JPG thumbnail of the pattern with proper layout."""
        # Calculate layout positions
        offsets = self._layout_pieces(pattern_pieces)
        
        # Calculate overall dimensions after layout
        all_points = []
        for piece_name, piece_data in pattern_pieces.items():
            points = self._extract_points(piece_data)
            if not points or piece_name not in offsets:
                continue
            offset_x, offset_y = offsets[piece_name]
            for x, y in points:
                all_points.append((x + offset_x, y + offset_y))
        
        if not all_points:
            return
        
        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        width = max_x - min_x + 2 * self.MARGIN
        height = max_y - min_y + 2 * self.MARGIN
        
        # Calculate thumbnail size maintaining aspect ratio
        aspect_ratio = width / height
        if aspect_ratio > 1:
            thumb_width = max_size
            thumb_height = int(max_size / aspect_ratio)
        else:
            thumb_height = max_size
            thumb_width = int(max_size * aspect_ratio)
        
        # Create figure
        fig = plt.figure(figsize=(thumb_width / 100, thumb_height / 100), dpi=100)
        ax = fig.add_subplot(111)
        
        # Set up coordinate system
        ax.set_xlim(min_x - self.MARGIN, max_x + self.MARGIN)
        ax.set_ylim(min_y - self.MARGIN, max_y + self.MARGIN)
        ax.set_aspect('equal')
        
        # Draw pattern pieces with layout
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
        for i, (piece_name, piece_data) in enumerate(pattern_pieces.items()):
            points = self._extract_points(piece_data)
            metadata = self._get_piece_metadata(piece_data)
            
            if not points or piece_name not in offsets:
                continue
            
            offset_x, offset_y = offsets[piece_name]
            xs = [p[0] + offset_x for p in points]
            ys = [p[1] + offset_y for p in points]
            color = colors[i % len(colors)]
            ax.plot(xs, ys, color=color, linewidth=2, label=metadata.get('label', piece_name))
            ax.fill(xs, ys, alpha=0.08, color=color)
        
        ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.2)
        ax.set_xlabel('Width (cm)', fontsize=8)
        ax.set_ylabel('Length (cm)', fontsize=8)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(loc='upper right', fontsize=8)
        
        # Save to JPG
        plt.tight_layout()
        plt.savefig(output_path, format='jpg', bbox_inches='tight', dpi=100, pil_kwargs={'quality': 85})
        plt.close(fig)
