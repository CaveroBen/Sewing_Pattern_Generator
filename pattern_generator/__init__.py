"""
Sewing Pattern Generator
A Python package for generating bespoke sewing patterns based on measurements.
"""

__version__ = "0.1.0"

from .measurements import Measurements, DefaultMeasurements
from .patterns import PatternGenerator

__all__ = ["Measurements", "DefaultMeasurements", "PatternGenerator"]
