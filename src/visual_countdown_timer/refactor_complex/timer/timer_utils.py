from .timer_settings import TimerConfig         # [x] Confirmed
import signal                                   # [x] Confirmed
import sys                                      # [x] Confirmed

class SupportUtils:
                                                # Edit this docstring.
    """
    Utility class providing common helper functions for timer operations.
    
    This class contains static methods for validation, formatting, and other
    utility operations used throughout the timer application. All methods
    are static as they don't require instance state.
    
    Methods:
        validate_and_convert_hour_format: Validates and converts hour format input
        clean_text: Removes leading/trailing whitespace and punctuation
        clear_terminal: Clears the terminal screen across different platforms
        sleep_until_next_loop: Sleeps until the next second boundary
    
    Example:
        >>> TimerUtils.validate_and_convert_hour_format("12")
        12
        >>> TimerUtils.clean_text("  hello!  ")
        'hello'
    """

    @staticmethod
    def clean_text(unformatted_text):
        """
        Removes leading and trailing spaces and common punctuation from a string.

        Args:
            unformatted_text (str): The string to be cleaned.

        Returns:
            clean_text (str): The cleaned string with specified characters removed from both ends.
        """
        characters_to_remove = " .,\"\'"
        clean_text = unformatted_text.strip(characters_to_remove)
        return clean_text
    
    @staticmethod
    def initialize_exit_handler():                                          # [x] Confirmed
        """Setup graceful shutdown handler for interrupt signals (typically Ctrl+C)."""
        def signal_handler(sig, frame):
            print("\n\nTimer stopped. Thank you for using Visual Countdown Timer!")
            sys.exit(TimerConfig.EXIT_SUCCESS)
        signal.signal(signal.SIGINT, signal_handler)
        
    @staticmethod
    def validate_hour_format(user_input):
        while True:
            try:
                user_hours_int = int(SupportUtils.clean_text((user_input)))
                if user_hours_int in TimerConfig.POSSIBLE_HOUR_DISPLAY_FORMATS:
                    return user_hours_int
                else:
                    raise ValueError
                
            except ValueError:
                print(f"\nError: Hour format must be either \"12\" or \"24\", written as a whole number. You typed: {user_input}\n")
                user_input = input('Please enter either \"12\" for 12-hour format, or \"24\" for 24-hour format: ')
