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

class TimerConfig:
    # Edit this docstring.
    """
    Configuration constants for the timer application.
    
    Contains internal constants that control application behavior such as
    display formatting, validation rules, and system settings. These values
    are not user-configurable and remain consistent across all timer sessions.
    
    Categories:
        - Display formatting (line thickness, indentation, progress bar)
        - Validation limits (min/max values, allowed formats) 
        - System behavior (exit codes, timing precision)
        - Character sets (cleanup characters, display symbols)
    
    Example:
        >>> TimerConfig.PROGRESS_BAR_WIDTH
        30
        >>> TimerConfig.POSSIBLE_HOUR_DISPLAY_FORMATS
        (12, 24)
    """

    # Exit code for successful program termination
    EXIT_SUCCESS = 0

    # Allowed values for user hour format preference (12-hour or 24-hour display)
    POSSIBLE_HOUR_DISPLAY_FORMATS = (12, 24)