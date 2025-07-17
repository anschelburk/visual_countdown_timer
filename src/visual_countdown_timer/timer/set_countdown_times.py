from .actions import (
    clean_text,
    confirm_user_input
    )

def _display_intro_text(runtime_status):
    """
    Displays introductory text to the user based on the current runtime status.

    If the status is 'initial', a welcome message and explanation of how the timer works
    is printed. If the status is 'update', a brief prompt for updating the countdown time
    is shown instead.

    Args:
        runtime_status (str): A string indicating the current context, expected to be
            either 'initial' or 'update'.

    Returns:
        None
    """
    if runtime_status == 'initial':
        print('Welcome to Visual Countdown Timer!')
        print('This timer counts down to a set number of minutes past each hour.')
        print('For example, if you enter \"25\", it will count down to 1:25, 2:25, etc.\n')

    elif runtime_status == 'update':
        print('\nWould you like to update the countdown time?')

def _get_valid_minute_input():
    """
    Prompts the user for input and returns a valid minute as an integer.

    Raises:
        ValueError: If the input cannot be converted to an integer or is not in the range 0–59.
    """
    user_input = clean_text(input("Please enter the number of minutes you'd like to count down to: "))
    
    try:
        minute = int(user_input)
        if not (0 <= minute < 60):
            raise ValueError
    except ValueError:
        raise ValueError("Error: the number of minutes must be a whole number between 0 and 59 (e.g., 0, 3, 25, 59).")

    return minute


def _user_confirms_countdown_time(minutes):
    """
    Loops until the user confirms ('y') or cancels ('n') the entered minute.
    
    Returns:
        bool: True if confirmed, False if not.
    """
    while True:
        user_confirmation = clean_text(confirm_user_input(minutes))
        if user_confirmation == 'y':
            return True
        elif user_confirmation == 'n':
            return False
        else:
            print("\nInvalid answer: Please enter 'y' for yes, or 'n' for no.")

def set_countdown_time(runtime_status):
    """
    Prompts the user to enter a single countdown time in minutes, confirms it,
    and returns it if valid. (60 will be added later downstream.)
    
    Args:
        runtime_status (str): 'initial' or 'update'
    
    Returns:
        int: A valid countdown minute (0–59)
    """

    _display_intro_text(runtime_status)

    while True:
        try:
            minutes = _get_valid_minute_input()
            if _user_confirms_countdown_time(minutes):
                return minutes
            else:
                print('')  # restart loop
        except ValueError as error_message:
            print(f"\nError: {error_message}\n")