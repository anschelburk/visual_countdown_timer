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

def get_valid_minute_input():
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

def set_countdown_time(runtime_status):
    
    """
    Please note: this function currently supports a user entering only a single countdown number of minutes.

    Returns a sorted list of countdown end times in minutes.

    Given a single countdown time in minutes, this function adds it to 
    a base set containing the value 60, then returns a sorted list of 
    the combined values.

    Args:
        runtime_status (str): A string set to one of two values: 'initial' or 'update'.
            This arg determines which text is shown to the user.

    Returns:
        countdown_times (list): A sorted list of integers representing countdown end times.
    """

    _display_intro_text(runtime_status)
    
    while True:

        user_input = clean_text(input(f'Please enter the number of minutes you\'d like to count down to: '))
        
        try:
            user_minutes = int(user_input)    
            if 0 <= user_minutes < 60:
                user_confirmation = ''
                while user_confirmation != 'y':
                    user_confirmation = clean_text(confirm_user_input(user_minutes))
                    if user_confirmation in ('y', 'n'):
                        print('')
                        break
                    else:
                        print('\nInvalid answer: Please enter \'y\' for yes, or \'n\' for no.')
                if user_confirmation == 'y':
                    break
            else:
                print("\nError: Please enter a number of minutes between 0 and 59.")
                print('')

        except ValueError:
            print("\nError: Please enter a valid number (e.g., 25).")
            print("This number must be written as an integer. \"3\" works; \"three\" doesn't.")
            print('')

    return user_minutes