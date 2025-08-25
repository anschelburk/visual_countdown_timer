"""
Contains all logic related to validating input.
"""

class InputIsValid:
    """
    Contains all validation checks.
    """

    def integer(user_input) -> bool:
        """
        Validates that a user input is an integer.
        """
        try:
            user_input = int(user_input)
            return True
        except ValueError:
            print("\nError: please enter a whole number.")
            print("(Please note that this program cannot convert words into numbers.)")
            return False