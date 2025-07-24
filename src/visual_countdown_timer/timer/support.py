from .constants import POSSIBLE_HOUR_DISPLAY_FORMATS
from datetime import datetime
import os
import time

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

def  clear_terminal():
    """
    Clears the terminal screen.
    Args: None.
    Returns: None.    
    """
    # Use 'clear' if running in a Unix-like shell on Windows (e.g., Git Bash or WSL)
    if 'bash' in os.environ.get('SHELL', '') or os.environ.get('TERM') == 'xterm':
        os.system('clear')

    # Use 'cls' if running in a native Windows terminal (e.g., Command Prompt or PowerShell)
    elif os.name == 'nt':
        os.system('cls')

    # Use 'clear' on macOS, Linux, or another Unix-based environment
    else:
        os.system('clear')

def sleep_until_next_loop():
        """
        Pauses execution just long enough to align the next loop iteration with the next full second.

        This function calculates the fractional time remaining in the current second 
        (based on the current microsecond) and sleeps for that duration. This helps 
        ensure that subsequent loops run approximately on second boundaries, resulting 
        in smoother and more consistent timing behavior.

        Args: None.
        Returns: None.
        """
        remaining_time_until_next_loop = 1 - (datetime.now().microsecond / 1_000_000)
        time.sleep(remaining_time_until_next_loop)

def validate_and_convert_hour_format(user_input):
    while True:
        try:
            user_hours_int = int(user_input)
            if user_hours_int in POSSIBLE_HOUR_DISPLAY_FORMATS:
                if user_hours_int == 12:
                    return 12
                elif user_hours_int == 24:
                    return 24
                else:
                    raise ValueError
            
        except ValueError:
            print(f"\nError: Hour format must be either \"12\" or \"24\", written as a whole number. You typed: '{user_input}'\n")
            user_input = ('Please enter either \"12\" for 12-hour format, or \"24\" for 24-hour format: ')