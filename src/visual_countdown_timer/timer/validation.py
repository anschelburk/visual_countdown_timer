from .settings import TimerConfig
from .system_utils import SystemUtils

"""
Contains all logic related to validating input.
"""

class InputIsValid:
    """
    Contains all validation checks.
    """

    def hour_display_format(user_input: int) -> bool:
        """
        Validates that a user input is an integer and a supported hour display format.
    
        Args:
            user_input (int): The integer value to validate as an hour format.
        
        Returns:
            bool: True if user_input is a valid hour display format (12 or 24),
                  False otherwise.
        """
        if user_input in TimerConfig.POSSIBLE_HOUR_FORMATS:
            return True
        else:
            SystemUtils.wrap_text(
                func_name='print',
                text_unformatted="\nError: please enter either 12 or 24 for the hour display format."
            )
            return False

    def integer(user_input) -> bool:
        """
        Validates that a user input is an integer.
        """
        try:
            user_input = int(user_input)
            return True
        
        except ValueError:
            SystemUtils.wrap_text(
                func_name = 'print',
                text_unformatted = (
                    "\nError: please enter a whole number." +
                    "\n(Please note that this program cannot convert words into numbers.)"
                )
            )
            return False
        
    def minutes_range(user_input: int) -> bool:
        """
        Validates that an integer is within the valid range for minutes.
        
        Checks if the provided integer falls within the standard minute range
        of 0 to 59 (inclusive of 0, exclusive of 60). This validation is used
        to ensure minute values are valid for time-related operations.
        
        Args:
            user_input (int): The integer value to validate as a minute value.
        
        Returns:
            bool: True if user_input is an integer between 0 and 59 (inclusive),
                  False otherwise.
        """
        if (0 <= user_input < 60):
            return True
        else:
            SystemUtils.wrap_text(
                func_name = 'print',
                text_unformatted = "\nError: please enter a whole number between 0 and 59."
            )
            return False
