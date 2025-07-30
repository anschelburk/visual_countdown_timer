"""
# Add docstring to module.
"""

class DisplaySettings:
    """
    Display configuration constants for the timer application interface.
    
    Contains constants that control the visual formatting and layout of
    the timer display, including line lengths, progress bar dimensions,
    indentation settings, and other visual element sizing. These settings
    determine the dimensions and spacing of display elements.
    
    Unlike user preferences (countdown time, hour format), these constants
    control the visual measurements and formatting parameters. They can be
    modified to customize the timer's appearance without affecting its
    core functionality.
    """

    # Number of spaces for text indentation
    INDENT_LENGTH = 2

    # Character length for horizontal divider lines
    LINE_LENGTH = 32
