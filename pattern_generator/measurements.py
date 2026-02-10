"""
Measurement classes for sewing pattern generation.
"""

from typing import Dict, Optional


class Measurements:
    """
    Class to store and validate body measurements for pattern generation.
    All measurements are in centimeters.
    """
    
    def __init__(self, measurements: Dict[str, float]):
        """
        Initialize measurements from a dictionary.
        
        Args:
            measurements: Dictionary of measurement names to values in cm
        """
        self.measurements = measurements
    
    def get(self, key: str, default: Optional[float] = None) -> Optional[float]:
        """Get a measurement value."""
        return self.measurements.get(key, default)
    
    def __getitem__(self, key: str) -> float:
        """Allow dictionary-style access."""
        return self.measurements[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if measurement exists."""
        return key in self.measurements
    
    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return self.measurements.copy()


class DefaultMeasurements:
    """
    Default measurement sets for different sizes and garment types.
    Based on standard sizing charts.
    """
    
    # Men's size Medium (chest 38-40 inches / 96.5-101.5 cm)
    MENS_MEDIUM = {
        # Upper body
        "chest": 99.0,
        "waist": 84.0,
        "hip": 99.0,
        "shoulder_width": 46.0,
        "across_back": 40.0,
        "neck": 39.0,
        "sleeve_length": 64.0,
        "arm_length": 84.0,
        "bicep": 33.0,
        "wrist": 17.0,
        
        # Lower body
        "inseam": 81.0,
        "outseam": 108.0,
        "thigh": 61.0,
        "knee": 40.0,
        "ankle": 23.0,
        "rise": 27.0,
        
        # Vertical
        "height": 178.0,
        "nape_to_waist": 48.0,
        "waist_to_hip": 20.0,
    }
    
    # Women's size Medium (UK 12-14 / US 8-10)
    WOMENS_MEDIUM = {
        # Upper body
        "bust": 96.5,
        "underbust": 79.0,
        "waist": 76.0,
        "hip": 101.5,
        "shoulder_width": 39.0,
        "across_back": 36.0,
        "neck": 35.0,
        "sleeve_length": 60.0,
        "arm_length": 78.0,
        "bicep": 28.0,
        "wrist": 15.0,
        
        # Lower body
        "inseam": 79.0,
        "outseam": 104.0,
        "thigh": 58.0,
        "knee": 38.0,
        "ankle": 22.0,
        "rise": 26.0,
        
        # Vertical
        "height": 168.0,
        "nape_to_waist": 42.0,
        "waist_to_hip": 20.0,
    }
    
    @classmethod
    def get_default(cls, gender: str = "mens", size: str = "medium") -> Measurements:
        """
        Get default measurements for a specific gender and size.
        
        Args:
            gender: "mens" or "womens"
            size: Currently only "medium" is supported
            
        Returns:
            Measurements object with default values
        """
        if gender.lower() == "mens":
            return Measurements(cls.MENS_MEDIUM.copy())
        elif gender.lower() == "womens":
            return Measurements(cls.WOMENS_MEDIUM.copy())
        else:
            raise ValueError(f"Unknown gender: {gender}. Use 'mens' or 'womens'")
