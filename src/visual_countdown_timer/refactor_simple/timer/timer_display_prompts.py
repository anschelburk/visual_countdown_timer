"""
# Add docstring for module.
"""

class DisplayForUser:
    """
    # Add docstring for class.
    """

    def __init__(self):
        pass

    @staticmethod
    def timer_app_welcome():
        """
        Prints the introductory text for the Visual Countdown Timer interface.
        Args: None.
        Returns: None.
        """
        print(THICK_HORIZONTAL_LINE)         # Define this.
        print('Visual Countdown Timer')
        print('Press Ctrl + C to exit.')     # Define this.
        print(f'{THICK_HORIZONTAL_LINE}\n')
