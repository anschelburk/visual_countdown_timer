from . import utils
from datetime import datetime, timedelta
import math
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
    clean_text = unformatted_text.strip(" .,\"\'")
    return clean_text

def  clear_terminal():
    """
    Clears the terminal screen.
    Args: None.
    Returns: None.    
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def confirm_user_input(input_to_confirm):
    """
    Displays the user's input and prompts for confirmation.

    Args:
        input_to_confirm (int): The number of minutes past the hour entered by the user.

    Returns:
        str: The user's confirmation input, converted to lowercase ('y' or 'n').
    """
    print(f'\nYou entered {input_to_confirm} minutes. The timer will count down to:')
    print(' | '.join(f'{hour:02}:{input_to_confirm:02}' for hour in range(1, 4)) + ' | etc.\n')
    user_confirmation = input('Is this correct? Please enter \'y\' or \'n\': ')
    return user_confirmation.lower()

def get_current_date():
    """
    Calculates the current date, formatted as follows: [Month] [Day], [Year].
    Args:
        None.
    Returns:
        current_date (datetime): a datetime object, formatted as described above.
    """
    current_date = datetime.now().strftime('%B %d, %Y')
    return current_date

def get_current_time():
    """
    Calculates the current time, formatted as follows: [Hour]:[Minute] [Timezone]
    Args:
        None.
    Returns:
        current_time (datetime): a datetime object, formatted as described above.
    """
    current_time = datetime.now().astimezone().strftime('%H:%M %Z')
    return current_time


def next_occurrence(current_datetime, target_minute):
    """
    Returns the next datetime where the minute equals target_minute.

    Args:
        current_datetime (datetime): The current datetime.
        target_minute (int): The target minute after the hour that the timer should count down to.

    Returns:
        next_occurrence (datetime): The next datetime where the minute equals target_minute.
    """
    if current_datetime.minute < target_minute:
        return current_datetime.replace(minute=target_minute, second=0, microsecond=0)
    else:
        next_hour = current_datetime + timedelta(hours=1)
        return next_hour.replace(minute=target_minute, second=0, microsecond=0)

def print_title_block(thick_dividing_line):
    """
    Prints the title block for the Visual Countdown Timer interface.
    Args:
        thick_dividing_line (str): A string of characters (e.g., "=" * 32) used as a visual divider.
    Returns:
        None.
    """
    print(thick_dividing_line)
    print('Visual Countdown Timer')
    print('Press Ctrl + C to exit.')
    print(f'{thick_dividing_line}\n')    

def progress_bar(remaining_time_in_seconds):
    """
    Generates a visual progress bar representing the remaining time until the next hour.

    Args:
        remaining_time_in_seconds (int): An integer which represents the total remaining time in seconds
            until the current timer finishes counting down.

    Returns:
        progress_bar_text (str):
            A visual progress bar composed of '#' and '.' characters showing the remaining
            amount of time until the current timer finishes counting down.

            Each '#' represents about 2 minutes of remaining time. (Every 2 minutes, the '#' character furthest
            to the right is replaced by a '.' character.) The '.' characters represent elapsed time. The
            number of minutes is rounded up if any seconds are left beyond a full minute to ensure a more
            intuitive countdown.

            The bar is 32 characters wide: 30 total '#' and '.' characters, enclosed in a left and right bracket.

            Examples:

            - 16 minutes, 00 seconds → 16 minutes → 8 filled ('#') characters and 22 empty ('.') characters, shown below.
                [########......................]
            
            - 16 minutes, 01 second  → 17 minutes → 9 filled ('#') characters and 21 empty ('.') characters, shown below.
                [#########.....................]
    """

    remaining_minutes_rounded = math.ceil(remaining_time_in_seconds / 60)
    progress_bar_full = '#' * round(remaining_minutes_rounded / 2)
    progress_bar_empty = '.' * (30 - round(remaining_minutes_rounded / 2))
    progress_bar_text = f'[{progress_bar_full}{progress_bar_empty}]'
    return progress_bar_text

def run_timer(countdown_times, thick_line, thin_line, indent):
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
            countdown_times (int): The number of minutes past each hour to count down to (e.g., 25 for 1:25, 2:25, etc.).
            thick_line (str): A visual divider string used to frame the header block.
            thin_line (str): A lighter divider string used to separate sections within the display.
            indent (str): A string used for indenting time values for consistent formatting.

        Returns:
            None: This function runs indefinitely and does not return.
        """
        while True:

            clear_terminal()

            now = datetime.now().astimezone()
            
            end_of_current_loop = next_occurrence(now, countdown_times)
            end_of_current_loop_formatted = end_of_current_loop.strftime('%H:%M %Z')

            remaining_time = end_of_current_loop - now
            total_remaining_time_in_seconds = int(remaining_time.total_seconds())
            remaining_minutes, remaining_seconds = divmod(total_remaining_time_in_seconds, 60)

            minutes_label = "minute" if remaining_minutes == 1 else "minutes"
            seconds_label = "second" if remaining_seconds == 1 else "seconds"
    
            print_title_block(thick_line)

            print(get_current_date())
            print(f'Current Time: {get_current_time()}')
            
            print('')
            print(thin_line)
            print(f'Countdown until {end_of_current_loop_formatted}:')
            print(thin_line)
            print(f'{indent}{remaining_minutes:02} {minutes_label}')
            print(f'{indent}{remaining_seconds:02} {seconds_label}')
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
                    if user_confirmation == 'n':
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