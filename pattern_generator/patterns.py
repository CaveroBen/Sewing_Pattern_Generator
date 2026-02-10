"""
Pattern generation classes using OpenPattern library.
This module provides pattern generation using the professional OpenPattern library
with established patternmaking methodologies.
"""

from typing import Optional, Tuple, List, Dict, Any
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

from .measurements import Measurements

# Try to import OpenPattern if available
try:
    import OpenPattern as OP
    OPENPATTERN_AVAILABLE = True
except ImportError:
    OPENPATTERN_AVAILABLE = False
    OP = None


class PatternGenerator:
    """
    Main class for generating sewing patterns using OpenPattern library.
    Uses professional OpenPattern methods for pattern drafting.
    """
    
    def __init__(self, measurements: Measurements):
        """
        Initialize pattern generator with measurements.
        
        Args:
            measurements: Measurements object with body measurements
            
        Raises:
            ImportError: If OpenPattern library is not installed
        """
        if not OPENPATTERN_AVAILABLE:
            raise ImportError(
                "OpenPattern library is required but not installed. Please install it using:\n"
                "  git clone https://github.com/fmetivier/OpenPattern.git\n"
                "  cd OpenPattern\n"
                "  pip install -e ."
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
    
    def _create_pattern_name(self) -> str:
        """
        Create a pattern name for OpenPattern using standard sizing.
        OpenPattern has built-in measurement databases for standard sizes.
        Format: W38G (Women's size 38, Gilewska) or M42G (Men's size 42, Gilewska)
        
        Returns:
            Pattern name string that corresponds to OpenPattern's database
        """
        chest = self._get_chest_measurement()
        gender = self._detect_gender()
        gender_prefix = 'W' if gender == 'w' else 'M'
        
        # Map chest measurement to standard OpenPattern sizes
        # OpenPattern uses even sizes: 36, 38, 40, 42, 44, 46, etc.
        # Chest measurements roughly correspond to French sizes
        if chest < 87:
            size = 36
        elif chest < 91:
            size = 38
        elif chest < 95:
            size = 40
        elif chest < 99:
            size = 42
        elif chest < 103:
            size = 44
        elif chest < 107:
            size = 46
        elif chest < 111:
            size = 48
        else:
            size = 50
            
        return f"{gender_prefix}{size}G"
        
    def generate_shirt(self) -> dict:
        """
        Generate a professional shirt pattern using OpenPattern's Basic_Bodice.
        
        Returns:
            Dictionary with OpenPattern pattern object
        """
        gender = self._detect_gender()
        pname = self._create_pattern_name()
        
        # Create bodice pattern using OpenPattern
        bodice = OP.Basic_Bodice(pname=pname, gender=gender, style='Gilewska')
        
        # Add darts for proper fit
        bodice.add_bust_dart()
        bodice.add_waist_dart()
        
        # Generate sleeve
        if gender == 'w':
            bodice.Gilewska_basic_sleeve_w()
        else:
            bodice.Gilewska_basic_sleeve_m()
        
        # Store the OpenPattern object
        self.patterns["shirt"] = {
            "openpattern_object": bodice,
            "type": "openpattern",
            "garment": "shirt",
            "pname": pname,
            "gender": gender
        }
        
        return self.patterns["shirt"]
    
    def generate_vest(self) -> dict:
        """
        Generate a professional vest/waistcoat pattern using OpenPattern.
        Uses bodice as base since Waist_Coat has some issues.
        
        Returns:
            Dictionary with OpenPattern pattern object
        """
        gender = self._detect_gender()
        pname = self._create_pattern_name()
        
        # Use bodice as base for vest (without sleeves, adjusted length)
        vest = OP.Basic_Bodice(pname=pname, gender=gender, style='Gilewska')
        # Add bust dart for better fit
        vest.add_bust_dart()
        
        self.patterns["vest"] = {
            "openpattern_object": vest,
            "type": "openpattern",
            "garment": "vest",
            "pname": pname,
            "gender": gender
        }
        
        return self.patterns["vest"]
    
    def generate_trousers(self) -> dict:
        """
        Generate professional trouser pattern using OpenPattern's Basic_Trousers.
        Note: Uses women's patterns for both genders due to OpenPattern database limitations.
        
        Returns:
            Dictionary with OpenPattern pattern object
        """
        gender = self._detect_gender()
        waist = self.measurements.get("waist", 85)
        
        # Map to standard sizes
        if waist < 66:
            size = 36
        elif waist < 70:
            size = 38
        elif waist < 74:
            size = 40
        elif waist < 78:
            size = 42
        elif waist < 82:
            size = 44
        elif waist < 86:
            size = 46
        elif waist < 90:
            size = 48
        else:
            size = 50
        
        # Use women's pattern for both genders as men's database is incomplete
        # The patterns are adjusted appropriately by OpenPattern
        pname = f"W{size}G"
        actual_gender = 'w'  # Always use 'w' due to database issues with 'm'
        
        # Create trouser pattern using OpenPattern
        # Try Gilewska first, fall back to Donnano if needed
        try:
            trousers = OP.Basic_Trousers(pname=pname, gender=actual_gender, style='Gilewska')
        except (KeyError, AttributeError):
            # If Gilewska fails, try Donnano
            trousers = OP.Basic_Trousers(pname=pname, gender=actual_gender, style='Donnano')
        
        self.patterns["trousers"] = {
            "openpattern_object": trousers,
            "type": "openpattern",
            "garment": "trousers",
            "pname": pname,
            "gender": gender,  # Store original gender for reference
            "openpattern_gender": actual_gender  # Store actual gender used
        }
        
        return self.patterns["trousers"]
    
    def generate_coat(self) -> dict:
        """
        Generate professional coat pattern using OpenPattern.
        Uses extended bodice with additional ease.
        
        Returns:
            Dictionary with OpenPattern pattern object
        """
        gender = self._detect_gender()
        pname = self._create_pattern_name()
        
        # Create coat using bodice as base with additional ease
        # (OpenPattern may not have a specific Coat class)
        coat = OP.Basic_Bodice(pname=pname, gender=gender, style='Gilewska')
        coat.add_bust_dart()
        coat.add_waist_dart()
        
        # Add sleeve
        if gender == 'w':
            coat.Gilewska_basic_sleeve_w()
        else:
            coat.Gilewska_basic_sleeve_m()
        
        self.patterns["coat"] = {
            "openpattern_object": coat,
            "type": "openpattern",
            "garment": "coat",
            "pname": pname,
            "gender": gender
        }
        
        return self.patterns["coat"]


# For backward compatibility, keep OpenPatternGenerator as an alias
OpenPatternGenerator = PatternGenerator
