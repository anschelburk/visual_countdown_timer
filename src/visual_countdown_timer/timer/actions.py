from .constants import (
    INDENT,
    THICK_HORIZONTAL_LINE,
    THIN_HORIZONTAL_LINE
    )
from .variables import (
    current_date,
    current_time,
    next_occurrence,
    progress_bar
    )
from .support import (
    clean_text,
    clear_terminal
    )
from datetime import datetime
import time

def confirm_hour_format():
    """
        Prompts the user to choose between 12-hour and 24-hour time display formats.
        Args: None.
        Returns: user_hours (int): The user's preferred time format, either 12 or 24.
    """
    print("\nWould you like the time to display as 12 hours or 24 hours?")
    print(f'{INDENT}{THIN_HORIZONTAL_LINE}')
    print(f"{INDENT}12 hours looks like this: 3:52pm")
    print(f"{INDENT}24 hours looks like this: 15:52")
    print(f'{INDENT}{THIN_HORIZONTAL_LINE}')
    user_input = input("Type \"12\" to format as 12 hours, or \"24\" to format as 24 hours: ")
    user_hours = int(clean_text(user_input))
    return user_hours

def confirm_user_input(input_to_confirm):
    """
    Displays the user's input and prompts for confirmation.

    Args:
        input_to_confirm (int): The number of minutes past the hour entered by the user.

    Returns:
        str: The user's confirmation input, converted to lowercase ('y' or 'n').
    """
    FIRST_HOUR_IN_RANGE = 1
    LAST_HOUR_IN_RANGE = 4

    print(f'\nYou entered {input_to_confirm} minutes. The timer will count down to:')
    print(' | '.join(f'{hour:02}:{input_to_confirm:02}' for hour in range(FIRST_HOUR_IN_RANGE, LAST_HOUR_IN_RANGE)) + ' | etc.\n')
    user_confirmation = input('Is this correct? Please enter \'y\' or \'n\': ')
    return user_confirmation.lower()

def format_time(unformatted_time, hours_format):
    """
    Formats a datetime object into a 12-hour or 24-hour time string with timezone.

    Args:
        unformatted_time (datetime): The datetime object to be formatted.
        hours_format (int): The preferred time format, either 12 or 24.

    Returns:
        formatted_time (str): The formatted time string.
    """
    if hours_format not in (12, 24):
        return 'Error (format_time()): Invalid time format.'
    else:
        timezone = unformatted_time.astimezone().strftime('%Z')
        if hours_format == 12:
            formatted_hours = unformatted_time.strftime('%I:%M')
            formatted_ampm = unformatted_time.strftime('%p').lower()
            formatted_time = f'{formatted_hours}{formatted_ampm} {timezone}'
        elif hours_format == 24:
            formatted_hours = unformatted_time.strftime('%H:%M')
            formatted_time = f'{formatted_hours} {timezone}'
        return formatted_time

def print_title_block():
    """
    Prints the title block for the Visual Countdown Timer interface.
    Args:
        thick_dividing_line (str): A string of characters (e.g., "=" * 32) used as a visual divider.
    Returns:
        None.
    """
    print(THICK_HORIZONTAL_LINE)
    print('Visual Countdown Timer')
    print('Press Ctrl + C to exit.')
    print(f'{THICK_HORIZONTAL_LINE}\n')    

def run_timer():
        """
        Continuously displays a live countdown timer to a specified minute past each hour.

        This function runs an infinite loop that:
        - Clears the terminal screen
        - Calculates the next occurrence of the specified countdown time
        - Displays the current date and time
        - Shows how much time remains until the next target time
        - Renders a visual progress bar
        - Waits just enough to sync with the next full second

        It uses various functions from this module, utils.py, to do these things.

        Args:
            None.

        Returns:
            None: This function runs indefinitely and does not return.
        """
        
        countdown_times = set_countdown_time('initial')
        hour_display_format = confirm_hour_format()
        
        while True:

            clear_terminal()

            now = datetime.now().astimezone()
            
            end_of_current_loop = next_occurrence(now, countdown_times)
            end_of_current_loop_formatted = format_time(end_of_current_loop, hour_display_format)

            remaining_time = end_of_current_loop - now
            total_remaining_time_in_seconds = int(remaining_time.total_seconds())
            remaining_minutes, remaining_seconds = divmod(total_remaining_time_in_seconds, 60)

            minutes_label = "minute" if remaining_minutes == 1 else "minutes"
            seconds_label = "second" if remaining_seconds == 1 else "seconds"
    
            print_title_block()

            print(current_date())
            print(f'Current Time: {current_time()}')
            
            print('')
            print(THIN_HORIZONTAL_LINE)
            print(f'Countdown until {end_of_current_loop_formatted}:')
            print(THIN_HORIZONTAL_LINE)
            print(f'{INDENT}{remaining_minutes:02} {minutes_label}')
            print(f'{INDENT}{remaining_seconds:02} {seconds_label}')
            print(progress_bar(total_remaining_time_in_seconds))
            
            sleep_until_next_loop()

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

    if runtime_status == 'initial':
        print('Welcome to Visual Countdown Timer!')
        print('This timer counts down to a set number of minutes past each hour.')
        print('For example, if you enter \"25\", it will count down to 1:25, 2:25, etc.\n')
        _new = ''

    elif runtime_status == 'update':
        print('\nWould you like to update the countdown time?')
        _new = ' new'
    
    while True:

        user_input = clean_text(input(f'Please enter the{_new} number of minutes you\'d like to count down to: '))
        
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