"""
Pattern generation classes for different garment types.
This module provides a simplified pattern generation system that can work
standalone or be extended with OpenPattern library if available.
"""

from typing import Optional, Tuple, List
import os

from .measurements import Measurements


class PatternGenerator:
    """
    Main class for generating sewing patterns.
    Creates basic pattern blocks that can be printed at full scale.
    """
    
    def __init__(self, measurements: Measurements):
        """
        Initialize pattern generator with measurements.
        
        Args:
            measurements: Measurements object with body measurements
        """
        self.measurements = measurements
        self.patterns = {}
        
    def generate_shirt(self) -> dict:
        """
        Generate a basic shirt pattern (front and back bodice).
        
        Returns:
            Dictionary with pattern pieces
        """
        m = self.measurements
        
        # Basic shirt bodice calculations
        # These are simplified pattern drafting formulas
        chest = m.get("chest", m.get("bust", 100))
        waist = m.get("waist", 85)
        shoulder = m.get("shoulder_width", 45)
        neck = m.get("neck", 38)
        length = m.get("nape_to_waist", 45)
        sleeve = m.get("sleeve_length", 60)
        
        # Calculate pattern dimensions with ease allowances
        ease = 10  # cm of ease for comfort
        half_chest = (chest + ease) / 2
        half_waist = (waist + ease) / 2
        
        patterns = {
            "front": self._create_bodice_front(half_chest, half_waist, shoulder, neck, length),
            "back": self._create_bodice_back(half_chest, half_waist, shoulder, neck, length),
            "sleeve": self._create_sleeve(sleeve, m.get("bicep", 32), m.get("wrist", 16)),
        }
        
        self.patterns["shirt"] = patterns
        return patterns
    
    def generate_vest(self) -> dict:
        """
        Generate a basic vest/waistcoat pattern.
        
        Returns:
            Dictionary with pattern pieces
        """
        m = self.measurements
        
        # Vest is similar to shirt but shorter and without sleeves
        chest = m.get("chest", m.get("bust", 100))
        waist = m.get("waist", 85)
        shoulder = m.get("shoulder_width", 45)
        neck = m.get("neck", 38)
        length = m.get("nape_to_waist", 45)
        
        ease = 8  # Less ease for a more fitted vest
        half_chest = (chest + ease) / 2
        half_waist = (waist + ease) / 2
        
        patterns = {
            "front": self._create_vest_front(half_chest, half_waist, shoulder, neck, length),
            "back": self._create_vest_back(half_chest, half_waist, shoulder, neck, length),
        }
        
        self.patterns["vest"] = patterns
        return patterns
    
    def generate_trousers(self) -> dict:
        """
        Generate basic trouser pattern.
        
        Returns:
            Dictionary with pattern pieces
        """
        m = self.measurements
        
        waist = m.get("waist", 85)
        hip = m.get("hip", 100)
        rise = m.get("rise", 27)
        inseam = m.get("inseam", 80)
        outseam = m.get("outseam", 107)
        
        ease = 8
        half_waist = (waist + ease) / 2
        half_hip = (hip + ease) / 2
        
        patterns = {
            "front": self._create_trouser_front(half_waist, half_hip, rise, inseam),
            "back": self._create_trouser_back(half_waist, half_hip, rise, inseam),
        }
        
        self.patterns["trousers"] = patterns
        return patterns
    
    def generate_coat(self) -> dict:
        """
        Generate basic coat pattern (extended shirt with more ease).
        
        Returns:
            Dictionary with pattern pieces
        """
        m = self.measurements
        
        chest = m.get("chest", m.get("bust", 100))
        waist = m.get("waist", 85)
        hip = m.get("hip", 100)
        shoulder = m.get("shoulder_width", 45)
        neck = m.get("neck", 38)
        length = m.get("nape_to_waist", 45) + 30  # Extended length for coat
        sleeve = m.get("sleeve_length", 60) + 5  # Slightly longer sleeve
        
        ease = 15  # More ease for coat to fit over other clothing
        half_chest = (chest + ease) / 2
        half_waist = (waist + ease) / 2
        
        patterns = {
            "front": self._create_coat_front(half_chest, half_waist, shoulder, neck, length),
            "back": self._create_coat_back(half_chest, half_waist, shoulder, neck, length),
            "sleeve": self._create_sleeve(sleeve, m.get("bicep", 32) + 5, m.get("wrist", 16) + 2),
        }
        
        self.patterns["coat"] = patterns
        return patterns
    
    def _create_bodice_front(self, half_chest: float, half_waist: float, 
                             shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create front bodice pattern piece."""
        neck_width = neck / 6
        neck_depth = neck / 6 + 1
        armhole_depth = length / 4
        
        # Define pattern outline points (x, y coordinates in cm)
        points = [
            (0, 0),  # Shoulder point
            (neck_width, 0),  # Neck width
            (neck_width, neck_depth),  # Neck depth
            (shoulder / 2, 0),  # Shoulder end
            (shoulder / 2, armhole_depth),  # Armhole depth
            (half_chest, armhole_depth + 5),  # Side seam at chest
            (half_waist, length),  # Side seam at waist
            (5, length),  # Center front at waist
            (0, neck_depth),  # Center front at neck
            (0, 0),  # Back to start
        ]
        return points
    
    def _create_bodice_back(self, half_chest: float, half_waist: float,
                            shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create back bodice pattern piece."""
        neck_width = neck / 6
        neck_depth = neck / 20
        armhole_depth = length / 4
        
        points = [
            (0, 0),
            (neck_width, 0),
            (neck_width, neck_depth),
            (shoulder / 2, 0),
            (shoulder / 2, armhole_depth),
            (half_chest, armhole_depth + 5),
            (half_waist, length),
            (5, length),
            (0, neck_depth),
            (0, 0),
        ]
        return points
    
    def _create_sleeve(self, length: float, bicep: float, wrist: float) -> List[Tuple[float, float]]:
        """Create sleeve pattern piece."""
        cap_height = bicep / 3
        half_bicep = bicep / 2
        half_wrist = wrist / 2
        
        points = [
            (half_bicep, 0),  # Center top
            (0, cap_height),  # Armhole curve
            (0, length - 5),  # Sleeve length
            (half_wrist, length),  # Wrist
            (bicep, length - 5),  # Other side
            (bicep, cap_height),  # Other armhole
            (half_bicep, 0),  # Back to top
        ]
        return points
    
    def _create_vest_front(self, half_chest: float, half_waist: float,
                           shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create front vest pattern piece (lower neckline, no sleeves)."""
        neck_width = neck / 5
        neck_depth = neck / 4  # Deeper V-neck for vest
        
        points = [
            (0, 0),
            (neck_width, 0),
            (neck_width, neck_depth),
            (shoulder / 2, 0),
            (half_chest, length / 3),  # Armhole for vest
            (half_waist, length),
            (5, length + 5),  # Slightly longer at center
            (0, neck_depth),
            (0, 0),
        ]
        return points
    
    def _create_vest_back(self, half_chest: float, half_waist: float,
                          shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create back vest pattern piece."""
        neck_width = neck / 6
        neck_depth = neck / 20
        
        points = [
            (0, 0),
            (neck_width, 0),
            (neck_width, neck_depth),
            (shoulder / 2, 0),
            (half_chest, length / 3),
            (half_waist, length),
            (5, length),
            (0, neck_depth),
            (0, 0),
        ]
        return points
    
    def _create_trouser_front(self, half_waist: float, half_hip: float,
                              rise: float, inseam: float) -> List[Tuple[float, float]]:
        """Create front trouser pattern piece."""
        crotch_extension = half_hip / 10
        knee = half_hip * 0.6
        ankle = half_hip * 0.45
        
        points = [
            (0, 0),  # Waist side
            (half_waist, 0),  # Waist center
            (half_waist + crotch_extension, rise),  # Crotch point
            (half_hip * 0.6, rise + inseam / 2),  # Knee
            (ankle / 2, rise + inseam),  # Ankle
            (0, rise + inseam),  # Ankle side
            (0, rise),  # Hip side
            (0, 0),  # Back to waist
        ]
        return points
    
    def _create_trouser_back(self, half_waist: float, half_hip: float,
                             rise: float, inseam: float) -> List[Tuple[float, float]]:
        """Create back trouser pattern piece."""
        crotch_extension = half_hip / 8
        knee = half_hip * 0.65
        ankle = half_hip * 0.5
        
        points = [
            (0, 0),
            (half_waist + 3, 0),  # Wider at back
            (half_waist + crotch_extension, rise + 3),  # Deeper crotch
            (half_hip * 0.65, rise + inseam / 2),
            (ankle / 2, rise + inseam),
            (0, rise + inseam),
            (0, rise),
            (0, 0),
        ]
        return points
    
    def _create_coat_front(self, half_chest: float, half_waist: float,
                           shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create front coat pattern piece (extended bodice)."""
        neck_width = neck / 6
        neck_depth = neck / 5  # Deeper for lapel
        armhole_depth = length / 5
        
        points = [
            (0, 0),
            (neck_width, 0),
            (neck_width, neck_depth),
            (shoulder / 2, 0),
            (shoulder / 2, armhole_depth),
            (half_chest, armhole_depth + 5),
            (half_chest + 2, length * 0.7),  # Slight A-line
            (5, length),
            (0, neck_depth),
            (0, 0),
        ]
        return points
    
    def _create_coat_back(self, half_chest: float, half_waist: float,
                          shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create back coat pattern piece."""
        neck_width = neck / 6
        neck_depth = neck / 20
        armhole_depth = length / 5
        
        points = [
            (0, 0),
            (neck_width, 0),
            (neck_width, neck_depth),
            (shoulder / 2, 0),
            (shoulder / 2, armhole_depth),
            (half_chest, armhole_depth + 5),
            (half_chest + 2, length * 0.7),
            (5, length),
            (0, neck_depth),
            (0, 0),
        ]
        return points
