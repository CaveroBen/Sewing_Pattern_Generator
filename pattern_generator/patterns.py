"""
Pattern generation classes for different garment types.
This module provides a simplified pattern generation system that can work
standalone or be extended with OpenPattern library if available.
"""

from typing import Optional, Tuple, List, Dict, Any
import os
import numpy as np
from scipy.interpolate import CubicSpline

from .measurements import Measurements

# Try to import OpenPattern if available
try:
    import OpenPattern as OP
    OPENPATTERN_AVAILABLE = True
except ImportError:
    OPENPATTERN_AVAILABLE = False


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
    
    @staticmethod
    def _smooth_curve(points: List[Tuple[float, float]], num_points: int = 20) -> List[Tuple[float, float]]:
        """
        Create a smooth curve through the given points using cubic spline interpolation.
        
        Args:
            points: List of (x, y) control points
            num_points: Number of points in the smooth curve
            
        Returns:
            List of interpolated points forming a smooth curve
        """
        if len(points) < 3:
            return points
        
        # Extract x and y coordinates
        xs = np.array([p[0] for p in points])
        ys = np.array([p[1] for p in points])
        
        # Create parameter t for parametric curve
        t = np.linspace(0, 1, len(points))
        t_smooth = np.linspace(0, 1, num_points)
        
        # Create cubic splines for x and y
        try:
            cs_x = CubicSpline(t, xs, bc_type='natural')
            cs_y = CubicSpline(t, ys, bc_type='natural')
            
            # Generate smooth curve
            xs_smooth = cs_x(t_smooth)
            ys_smooth = cs_y(t_smooth)
            
            return list(zip(xs_smooth, ys_smooth))
        except:
            # Fallback to linear interpolation if spline fails
            return points
    
    @staticmethod
    def _create_curve_between(start: Tuple[float, float], end: Tuple[float, float], 
                             control: Tuple[float, float], num_points: int = 15) -> List[Tuple[float, float]]:
        """
        Create a smooth curve between two points using a control point (quadratic Bezier).
        
        Args:
            start: Starting point (x, y)
            end: Ending point (x, y)
            control: Control point that defines the curve (x, y)
            num_points: Number of points in the curve
            
        Returns:
            List of points forming a smooth curve
        """
        t_values = np.linspace(0, 1, num_points)
        curve_points = []
        
        for t in t_values:
            # Quadratic Bezier formula: B(t) = (1-t)^2*P0 + 2(1-t)t*P1 + t^2*P2
            x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
            y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
            curve_points.append((x, y))
        
        return curve_points
        
    def generate_shirt(self) -> dict:
        """
        Generate a basic shirt pattern (front and back bodice) with proper curves and metadata.
        
        Returns:
            Dictionary with pattern pieces including metadata
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
            "front": {
                "points": self._create_bodice_front(half_chest, half_waist, shoulder, neck, length),
                "label": "FRONT BODICE",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
            "back": {
                "points": self._create_bodice_back(half_chest, half_waist, shoulder, neck, length),
                "label": "BACK BODICE",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
            "sleeve": {
                "points": self._create_sleeve(sleeve, m.get("bicep", 32), m.get("wrist", 16)),
                "label": "SLEEVE",
                "cutting": "Cut 2",
                "grainline": "vertical",
                "notches": []
            },
        }
        
        self.patterns["shirt"] = patterns
        return patterns
    
    def generate_vest(self) -> dict:
        """
        Generate a basic vest/waistcoat pattern with metadata.
        
        Returns:
            Dictionary with pattern pieces including metadata
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
            "front": {
                "points": self._create_vest_front(half_chest, half_waist, shoulder, neck, length),
                "label": "VEST FRONT",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
            "back": {
                "points": self._create_vest_back(half_chest, half_waist, shoulder, neck, length),
                "label": "VEST BACK",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
        }
        
        self.patterns["vest"] = patterns
        return patterns
    
    def generate_trousers(self) -> dict:
        """
        Generate basic trouser pattern with metadata.
        
        Returns:
            Dictionary with pattern pieces including metadata
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
            "front": {
                "points": self._create_trouser_front(half_waist, half_hip, rise, inseam),
                "label": "TROUSER FRONT",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
            "back": {
                "points": self._create_trouser_back(half_waist, half_hip, rise, inseam),
                "label": "TROUSER BACK",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
        }
        
        self.patterns["trousers"] = patterns
        return patterns
    
    def generate_coat(self) -> dict:
        """
        Generate basic coat pattern (extended shirt with more ease) with metadata.
        
        Returns:
            Dictionary with pattern pieces including metadata
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
            "front": {
                "points": self._create_coat_front(half_chest, half_waist, shoulder, neck, length),
                "label": "COAT FRONT",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
            "back": {
                "points": self._create_coat_back(half_chest, half_waist, shoulder, neck, length),
                "label": "COAT BACK",
                "cutting": "Cut 2 (1 pair)",
                "grainline": "vertical",
                "notches": []
            },
            "sleeve": {
                "points": self._create_sleeve(sleeve, m.get("bicep", 32) + 5, m.get("wrist", 16) + 2),
                "label": "COAT SLEEVE",
                "cutting": "Cut 2",
                "grainline": "vertical",
                "notches": []
            },
        }
        
        self.patterns["coat"] = patterns
        return patterns
    
    def _create_bodice_front(self, half_chest: float, half_waist: float, 
                             shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create front bodice pattern piece with smooth curves."""
        neck_width = neck / 6
        neck_depth = neck / 6 + 1
        armhole_depth = length / 4
        shoulder_end = shoulder / 2
        
        # Define key points
        center_neck = (0, 0)
        neck_side = (neck_width, 0)
        neck_bottom = (neck_width, neck_depth)
        shoulder_tip = (shoulder_end, -1)  # Slight drop for shoulder slope
        armhole_top = (shoulder_end, armhole_depth * 0.3)
        underarm = (half_chest, armhole_depth + 5)
        side_waist = (half_waist, length)
        center_waist = (5, length)
        center_bottom = (0, neck_depth)
        
        # Create smooth neckline curve
        neckline = self._create_curve_between(
            center_neck, neck_side, 
            (neck_width * 0.5, -0.5),  # Control point for curved neckline
            num_points=10
        )
        
        # Create smooth armhole curve
        armhole_points = [shoulder_tip, armhole_top, underarm]
        armhole_curve = self._smooth_curve(armhole_points, num_points=15)
        
        # Assemble the complete pattern outline
        points = (
            neckline +
            [(neck_side[0], neck_side[1])] +
            armhole_curve +
            [(underarm[0], underarm[1]), side_waist, center_waist, center_bottom] +
            [(center_neck[0], center_neck[1])]
        )
        
        return points
    
    def _create_bodice_back(self, half_chest: float, half_waist: float,
                            shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create back bodice pattern piece with smooth curves."""
        neck_width = neck / 6
        neck_depth = neck / 20  # Shallower neckline for back
        armhole_depth = length / 4
        shoulder_end = shoulder / 2
        
        # Define key points
        center_neck = (0, 0)
        neck_side = (neck_width, 0)
        shoulder_tip = (shoulder_end, -0.5)  # Slight slope
        armhole_top = (shoulder_end, armhole_depth * 0.3)
        underarm = (half_chest, armhole_depth + 5)
        side_waist = (half_waist, length)
        center_waist = (5, length)
        center_top = (0, neck_depth)
        
        # Create smooth back neckline
        back_neckline = self._create_curve_between(
            center_neck, neck_side,
            (neck_width * 0.5, -0.3),  # Gentler curve for back neck
            num_points=8
        )
        
        # Create smooth armhole curve
        armhole_points = [shoulder_tip, armhole_top, underarm]
        armhole_curve = self._smooth_curve(armhole_points, num_points=15)
        
        # Assemble complete pattern
        points = (
            back_neckline +
            [(neck_side[0], neck_side[1])] +
            armhole_curve +
            [(underarm[0], underarm[1]), side_waist, center_waist, center_top] +
            [(center_neck[0], center_neck[1])]
        )
        
        return points
    
    def _create_sleeve(self, length: float, bicep: float, wrist: float) -> List[Tuple[float, float]]:
        """Create sleeve pattern piece with smooth sleeve cap curve."""
        cap_height = bicep / 3
        half_bicep = bicep / 2
        half_wrist = wrist / 2
        
        # Define key points for sleeve cap (the curved top)
        cap_center = (half_bicep, 0)
        cap_left_mid = (half_bicep * 0.3, cap_height * 0.7)
        cap_left = (0, cap_height)
        underarm_left = (0, length - 5)
        wrist_left = (half_wrist * 0.7, length)
        wrist_center = (half_bicep, length)
        wrist_right = (bicep - half_wrist * 0.7, length)
        underarm_right = (bicep, length - 5)
        cap_right = (bicep, cap_height)
        cap_right_mid = (bicep - half_bicep * 0.3, cap_height * 0.7)
        
        # Create smooth sleeve cap curve
        left_cap_points = [cap_center, cap_left_mid, cap_left]
        left_cap = self._smooth_curve(left_cap_points, num_points=12)
        
        right_cap_points = [cap_center, cap_right_mid, cap_right]
        right_cap = self._smooth_curve(right_cap_points, num_points=12)
        
        # Assemble sleeve pattern
        points = (
            left_cap +
            [underarm_left, wrist_left, wrist_center, wrist_right, underarm_right] +
            list(reversed(right_cap))
        )
        
        return points
    
    def _create_vest_front(self, half_chest: float, half_waist: float,
                           shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create front vest pattern piece with V-neck and smooth curves."""
        neck_width = neck / 5
        neck_depth = neck / 4  # Deeper V-neck for vest
        shoulder_end = shoulder / 2
        
        # Key points
        center_top = (0, 0)
        v_neck_point = (neck_width, neck_depth)  # Point of V
        shoulder_tip = (shoulder_end, -1)
        armhole_mid = (shoulder_end, length / 4)
        underarm = (half_chest, length / 3)
        side_waist = (half_waist, length)
        center_waist = (5, length + 5)  # Slightly longer at center
        
        # Create V-neckline (straight lines for V)
        v_neck = [(center_top), v_neck_point]
        
        # Create smooth armhole
        armhole_points = [shoulder_tip, armhole_mid, underarm]
        armhole = self._smooth_curve(armhole_points, num_points=12)
        
        # Assemble pattern
        points = (
            v_neck +
            armhole +
            [side_waist, center_waist] +
            [(center_top[0], center_top[1])]
        )
        
        return points
    
    def _create_vest_back(self, half_chest: float, half_waist: float,
                          shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create back vest pattern piece with smooth curves."""
        neck_width = neck / 6
        neck_depth = neck / 20
        shoulder_end = shoulder / 2
        
        # Key points
        center_top = (0, 0)
        neck_side = (neck_width, 0)
        shoulder_tip = (shoulder_end, -0.5)
        armhole_mid = (shoulder_end, length / 4)
        underarm = (half_chest, length / 3)
        side_waist = (half_waist, length)
        center_waist = (5, length)
        center_neck = (0, neck_depth)
        
        # Create smooth neckline
        neckline = self._create_curve_between(
            center_top, neck_side,
            (neck_width * 0.5, -0.2),
            num_points=8
        )
        
        # Create smooth armhole
        armhole_points = [shoulder_tip, armhole_mid, underarm]
        armhole = self._smooth_curve(armhole_points, num_points=12)
        
        # Assemble pattern
        points = (
            neckline +
            [(neck_side[0], neck_side[1])] +
            armhole +
            [side_waist, center_waist, center_neck] +
            [(center_top[0], center_top[1])]
        )
        
        return points
    
    def _create_trouser_front(self, half_waist: float, half_hip: float,
                              rise: float, inseam: float) -> List[Tuple[float, float]]:
        """Create front trouser pattern piece with smooth curves."""
        crotch_extension = half_hip / 10
        knee = half_hip * 0.6
        ankle = half_hip * 0.45
        
        # Key points
        waist_side = (0, 0)
        waist_center = (half_waist, 0)
        crotch = (half_waist + crotch_extension, rise)
        knee_inside = (half_hip * 0.6, rise + inseam / 2)
        ankle_inside = (ankle / 2, rise + inseam)
        ankle_outside = (0, rise + inseam)
        hip_side = (0, rise)
        
        # Create smooth crotch curve
        crotch_points = [waist_center, crotch, knee_inside]
        crotch_curve = self._smooth_curve(crotch_points, num_points=15)
        
        # Assemble pattern
        points = (
            [waist_side, waist_center] +
            crotch_curve +
            [ankle_inside, ankle_outside, hip_side, waist_side]
        )
        
        return points
    
    def _create_trouser_back(self, half_waist: float, half_hip: float,
                             rise: float, inseam: float) -> List[Tuple[float, float]]:
        """Create back trouser pattern piece with smooth curves."""
        crotch_extension = half_hip / 8
        knee = half_hip * 0.65
        ankle = half_hip * 0.5
        
        # Key points
        waist_side = (0, 0)
        waist_center = (half_waist + 3, 0)  # Wider at back
        crotch = (half_waist + crotch_extension, rise + 3)  # Deeper crotch
        knee_inside = (half_hip * 0.65, rise + inseam / 2)
        ankle_inside = (ankle / 2, rise + inseam)
        ankle_outside = (0, rise + inseam)
        hip_side = (0, rise)
        
        # Create smooth crotch curve
        crotch_points = [waist_center, crotch, knee_inside]
        crotch_curve = self._smooth_curve(crotch_points, num_points=15)
        
        # Assemble pattern
        points = (
            [waist_side, waist_center] +
            crotch_curve +
            [ankle_inside, ankle_outside, hip_side, waist_side]
        )
        
        return points
    
    def _create_coat_front(self, half_chest: float, half_waist: float,
                           shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create front coat pattern piece (extended bodice) with smooth curves."""
        neck_width = neck / 6
        neck_depth = neck / 5  # Deeper for lapel
        armhole_depth = length / 5
        shoulder_end = shoulder / 2
        
        # Key points
        center_top = (0, 0)
        neck_side = (neck_width, 0)
        neck_bottom = (neck_width, neck_depth)
        shoulder_tip = (shoulder_end, -1)
        armhole_top = (shoulder_end, armhole_depth)
        underarm = (half_chest, armhole_depth + 5)
        side_hip = (half_chest + 2, length * 0.7)  # Slight A-line
        center_hem = (5, length)
        center_neck = (0, neck_depth)
        
        # Create smooth neckline/lapel
        neckline = self._create_curve_between(
            center_top, neck_side,
            (neck_width * 0.5, -0.5),
            num_points=10
        )
        
        # Create smooth armhole
        armhole_points = [shoulder_tip, armhole_top, underarm]
        armhole = self._smooth_curve(armhole_points, num_points=15)
        
        # Assemble pattern
        points = (
            neckline +
            [(neck_side[0], neck_side[1])] +
            armhole +
            [side_hip, center_hem, center_neck] +
            [(center_top[0], center_top[1])]
        )
        
        return points
    
    def _create_coat_back(self, half_chest: float, half_waist: float,
                          shoulder: float, neck: float, length: float) -> List[Tuple[float, float]]:
        """Create back coat pattern piece with smooth curves."""
        neck_width = neck / 6
        neck_depth = neck / 20
        armhole_depth = length / 5
        shoulder_end = shoulder / 2
        
        # Key points
        center_top = (0, 0)
        neck_side = (neck_width, 0)
        shoulder_tip = (shoulder_end, -0.5)
        armhole_top = (shoulder_end, armhole_depth)
        underarm = (half_chest, armhole_depth + 5)
        side_hip = (half_chest + 2, length * 0.7)
        center_hem = (5, length)
        center_neck = (0, neck_depth)
        
        # Create smooth neckline
        neckline = self._create_curve_between(
            center_top, neck_side,
            (neck_width * 0.5, -0.3),
            num_points=8
        )
        
        # Create smooth armhole
        armhole_points = [shoulder_tip, armhole_top, underarm]
        armhole = self._smooth_curve(armhole_points, num_points=15)
        
        # Assemble pattern
        points = (
            neckline +
            [(neck_side[0], neck_side[1])] +
            armhole +
            [side_hip, center_hem, center_neck] +
            [(center_top[0], center_top[1])]
        )
        
        return points


class OpenPatternGenerator:
    """
    Pattern generator using the OpenPattern library for formal pattern drafting.
    This class provides a more sophisticated pattern generation method based on
    established patternmaking methodologies.
    
    Requires OpenPattern library to be installed:
    git clone https://github.com/fmetivier/OpenPattern.git
    cd OpenPattern
    python setup.py install
    """
    
    def __init__(self, measurements: Measurements):
        """
        Initialize OpenPattern generator with measurements.
        
        Args:
            measurements: Measurements object with body measurements
            
        Raises:
            ImportError: If OpenPattern library is not installed
        """
        if not OPENPATTERN_AVAILABLE:
            raise ImportError(
                "OpenPattern library is not installed. Please install it using:\n"
                "  git clone https://github.com/fmetivier/OpenPattern.git\n"
                "  cd OpenPattern\n"
                "  python setup.py install"
            )
        
        self.measurements = measurements
        self.patterns = {}
    
    def _get_chest_measurement(self) -> float:
        """
        Get chest/bust measurement with appropriate fallback.
        
        Returns:
            Chest measurement in cm (defaults to 100 if not found)
        """
        return self.measurements.get("chest", self.measurements.get("bust", 100))
    
    def _detect_gender(self) -> str:
        """
        Detect gender from measurements for OpenPattern.
        
        OpenPattern uses 'w' for women's and 'm' for men's patterns.
        This is a heuristic based on typical measurement names.
        
        Returns:
            'w' for women's, 'm' for men's
        """
        # Women's measurements typically include 'bust' and/or 'underbust'
        # Men's measurements typically use 'chest' instead
        if 'underbust' in self.measurements.measurements or \
           ('bust' in self.measurements.measurements and 'chest' not in self.measurements.measurements):
            return 'w'
        return 'm'
        
    def generate_shirt(self) -> dict:
        """
        Generate a formal shirt pattern using OpenPattern's Basic_Bodice.
        
        Returns:
            Dictionary with pattern pieces
        """
        # Map our measurements to OpenPattern format
        chest = self._get_chest_measurement()
        gender = self._detect_gender()
        
        # Create a custom measurement name for OpenPattern
        # OpenPattern uses specific size names like "W36G" or "M42G"
        pname = f"custom_{int(chest)}"
        
        # Generate bodice pattern using OpenPattern
        pattern = OP.Basic_Bodice(pname=pname, gender=gender, style='Gilewska')
        
        # Add darts for proper fit
        pattern.add_bust_dart()
        pattern.add_waist_dart()
        
        # Store the OpenPattern object for later export
        self.patterns["shirt"] = {
            "bodice": pattern,
            "type": "openpattern",
            "garment": "shirt"
        }
        
        return self.patterns["shirt"]
    
    def generate_vest(self) -> dict:
        """
        Generate a formal vest pattern using OpenPattern.
        
        Returns:
            Dictionary with pattern pieces
        """
        chest = self._get_chest_measurement()
        gender = self._detect_gender()
        pname = f"custom_{int(chest)}"
        
        # Use bodice as base for vest
        pattern = OP.Basic_Bodice(pname=pname, gender=gender, style='Gilewska')
        pattern.add_bust_dart()
        
        self.patterns["vest"] = {
            "bodice": pattern,
            "type": "openpattern",
            "garment": "vest"
        }
        
        return self.patterns["vest"]
    
    def generate_trousers(self) -> dict:
        """
        Generate formal trouser pattern using OpenPattern.
        
        Returns:
            Dictionary with pattern pieces
        """
        waist = self.measurements.get("waist", 85)
        gender = self._detect_gender()
        pname = f"custom_{int(waist)}"
        
        # OpenPattern has trouser patterns
        # Using basic trouser block
        try:
            pattern = OP.Basic_Trouser(pname=pname, gender=gender, style='Gilewska')
        except (AttributeError, NameError):
            # If Basic_Trouser is not available, fall back to a simpler approach
            # Some OpenPattern versions may not have all garment types
            raise NotImplementedError(
                "OpenPattern trouser generation not available in this version. "
                "Use the basic PatternGenerator for trousers."
            )
        
        self.patterns["trousers"] = {
            "trouser": pattern,
            "type": "openpattern",
            "garment": "trousers"
        }
        
        return self.patterns["trousers"]
    
    def generate_coat(self) -> dict:
        """
        Generate formal coat pattern using OpenPattern.
        
        Returns:
            Dictionary with pattern pieces
        """
        chest = self._get_chest_measurement()
        gender = self._detect_gender()
        pname = f"custom_{int(chest)}"
        
        # Use extended bodice for coat
        pattern = OP.Basic_Bodice(pname=pname, gender=gender, style='Gilewska')
        pattern.add_bust_dart()
        pattern.add_waist_dart()
        
        self.patterns["coat"] = {
            "bodice": pattern,
            "type": "openpattern",
            "garment": "coat"
        }
        
        return self.patterns["coat"]
    
    @staticmethod
    def is_available() -> bool:
        """
        Check if OpenPattern library is available.
        
        Returns:
            True if OpenPattern is installed, False otherwise
        """
        return OPENPATTERN_AVAILABLE
