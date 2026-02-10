"""
Export functionality for sewing patterns.
Handles PDF generation (full-size and tiled A4) and JPG thumbnail creation.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
import numpy as np
from PIL import Image
from typing import List, Tuple, Optional
import os
import io
import math


class PatternExporter:
    """
    Class for exporting patterns to PDF and JPG formats.
    """
    
    # A4 dimensions in cm
    A4_WIDTH = 21.0
    A4_HEIGHT = 29.7
    
    # Margins in cm
    MARGIN = 1.0
    
    def __init__(self, output_dir: str = "output"):
        """
        Initialize exporter.
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_pattern(self, pattern_pieces: dict, garment_type: str,
                      title: str, full_pdf: bool = True, 
                      tiled_pdf: bool = False, jpg: bool = True) -> dict:
        """
        Export pattern pieces to various formats.
        
        Args:
            pattern_pieces: Dictionary of pattern piece names to point lists
            garment_type: Type of garment (shirt, vest, etc.)
            title: Title for the pattern
            full_pdf: Generate full-size PDF
            tiled_pdf: Generate A4-tiled PDF
            jpg: Generate JPG thumbnail
            
        Returns:
            Dictionary of generated file paths
        """
        output_files = {}
        
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
    
    def _create_full_pdf(self, pattern_pieces: dict, title: str, output_path: str):
        """Create a full-size PDF of the pattern."""
        # Calculate overall dimensions
        all_points = []
        for points in pattern_pieces.values():
            all_points.extend(points)
        
        if not all_points:
            return
        
        xs = [p[0] for p in all_points]
        ys = [p[1] for p in all_points]
        
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        width = max_x - min_x + 2 * self.MARGIN
        height = max_y - min_y + 2 * self.MARGIN
        
        # Create figure with size in inches (convert from cm)
        fig = plt.figure(figsize=(width / 2.54, height / 2.54), dpi=100)
        ax = fig.add_subplot(111)
        
        # Set up coordinate system (1:1 scale in cm)
        ax.set_xlim(min_x - self.MARGIN, max_x + self.MARGIN)
        ax.set_ylim(min_y - self.MARGIN, max_y + self.MARGIN)
        ax.set_aspect('equal')
        
        # Draw pattern pieces
        colors = ['blue', 'green', 'red', 'purple', 'orange']
        for i, (piece_name, points) in enumerate(pattern_pieces.items()):
            if points:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                color = colors[i % len(colors)]
                ax.plot(xs, ys, color=color, linewidth=2, label=piece_name)
                ax.fill(xs, ys, alpha=0.1, color=color)
        
        # Add grid (1cm grid)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.set_xlabel('Width (cm)')
        ax.set_ylabel('Length (cm)')
        ax.set_title(title, fontsize=16, fontweight='bold')
        ax.legend(loc='upper right')
        
        # Add scale reference (10cm line)
        scale_x = min_x + self.MARGIN
        scale_y = min_y + self.MARGIN / 2
        ax.plot([scale_x, scale_x + 10], [scale_y, scale_y], 'k-', linewidth=3)
        ax.text(scale_x + 5, scale_y - 0.5, '10 cm', ha='center', fontsize=10, fontweight='bold')
        
        # Save to PDF
        plt.savefig(output_path, format='pdf', bbox_inches='tight', dpi=100)
        plt.close(fig)
    
    def _create_tiled_pdf(self, pattern_pieces: dict, title: str, output_path: str):
        """Create a tiled PDF for printing on A4 sheets."""
        # Calculate overall dimensions
        all_points = []
        for points in pattern_pieces.values():
            all_points.extend(points)
        
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
                    colors = ['blue', 'green', 'red', 'purple', 'orange']
                    for i, (piece_name, points) in enumerate(pattern_pieces.items()):
                        if points:
                            xs = [p[0] for p in points]
                            ys = [p[1] for p in points]
                            color = colors[i % len(colors)]
                            ax.plot(xs, ys, color=color, linewidth=2)
                            ax.fill(xs, ys, alpha=0.1, color=color)
                    
                    # Add grid
                    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)
                    ax.set_xlabel('Width (cm)')
                    ax.set_ylabel('Length (cm)')
                    
                    # Add tile information
                    tile_title = f"{title} - Tile ({tile_x + 1}, {tile_y + 1}) of ({tiles_x}, {tiles_y})"
                    ax.set_title(tile_title, fontsize=12)
                    
                    # Add alignment marks at corners
                    for corner_x in [tile_min_x, tile_max_x]:
                        for corner_y in [tile_min_y, tile_max_y]:
                            ax.plot(corner_x, corner_y, 'k+', markersize=10, markeredgewidth=2)
                    
                    pdf.savefig(fig, bbox_inches='tight', dpi=100)
                    plt.close(fig)
    
    def _create_jpg(self, pattern_pieces: dict, title: str, output_path: str, max_size: int = 1200):
        """Create a JPG thumbnail of the pattern."""
        # Calculate overall dimensions
        all_points = []
        for points in pattern_pieces.values():
            all_points.extend(points)
        
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
        
        # Draw pattern pieces
        colors = ['blue', 'green', 'red', 'purple', 'orange']
        for i, (piece_name, points) in enumerate(pattern_pieces.items()):
            if points:
                xs = [p[0] for p in points]
                ys = [p[1] for p in points]
                color = colors[i % len(colors)]
                ax.plot(xs, ys, color=color, linewidth=2, label=piece_name)
                ax.fill(xs, ys, alpha=0.1, color=color)
        
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.3)
        ax.set_xlabel('Width (cm)', fontsize=8)
        ax.set_ylabel('Length (cm)', fontsize=8)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(loc='upper right', fontsize=8)
        
        # Save to JPG
        plt.savefig(output_path, format='jpg', bbox_inches='tight', dpi=100)
        plt.close(fig)
