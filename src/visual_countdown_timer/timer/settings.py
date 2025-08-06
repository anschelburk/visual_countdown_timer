"""
Configuration settings for the Visual Countdown Timer.

This module defines configuration classes containing settings for
display formatting, timer behavior, and validation parameters.
"""

class DisplaySettings:
    """Configuration for display formatting and visual elements."""
    
    # Line formatting
    LINE_THICKNESS = 32
    INDENT_LENGTH = 2
    
    # Progress bar settings
    PROGRESS_BAR_WIDTH = 30


class TimerConfig:
    """Configuration for timer behavior and validation."""
    
    # Time format options
    POSSIBLE_HOUR_FORMATS = (12, 24)
    
    # Input validation
    MIN_MINUTES = 0
    MAX_MINUTES = 59
