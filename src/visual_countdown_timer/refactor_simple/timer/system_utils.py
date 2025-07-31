from datetime import datetime
import os
import signal
import sys
import time

class SystemUtils:
    """Handles system-level operations like terminal clearing and timing."""
    
    @staticmethod
    def clean_text(unformatted_text):
        """
        Removes leading and trailing spaces and common punctuation from a string.

        Args:
            unformatted_text (str): The string to be cleaned.

        Returns:
            clean_text (str): The cleaned string with specified characters removed from both ends.
        """
        characters_to_remove = " .,\"'"
        clean_text = unformatted_text.strip(characters_to_remove)
        return clean_text
    
    @staticmethod
    def clear_terminal():
        """Clears the terminal screen."""
        # Use 'clear' if running in a Unix-like shell on Windows
        if 'bash' in os.environ.get('SHELL', '') or os.environ.get('TERM') == 'xterm':
            os.system('clear')
        # Use 'cls' if running in a native Windows terminal
        elif os.name == 'nt':
            os.system('cls')
        # Use 'clear' on macOS, Linux, or other Unix-based environments
        else:
            os.system('clear')
    
    @staticmethod
    def sleep_until_next_second():
        """
        Pauses execution to align next loop with the next full second.
        
        Calculates fractional time remaining in current second and sleeps
        for that duration to ensure loops run on second boundaries.
        """
        remaining_time_until_next_loop = 1 - (datetime.now().microsecond / 1_000_000)
        time.sleep(remaining_time_until_next_loop)
    
    @staticmethod
    def initialize_exit_handler():
        """Setup graceful shutdown handler for interrupt signals (typically Ctrl+C)."""

        def signal_handler(sig, frame):
            print("\n\nTimer stopped. Thank you for using Visual Countdown Timer!")
            sys.exit(TimerConfig.EXIT_SUCCESS)
        signal.signal(signal.SIGINT, signal_handler)

