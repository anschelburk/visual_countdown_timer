from .constants import (
    INDENT,
    POSSIBLE_HOUR_DISPLAY_FORMATS,
    THICK_HORIZONTAL_LINE,
    THIN_HORIZONTAL_LINE
    )
from .variables import (
    next_occurrence,
    progress_bar,
    total_remaining_seconds
    )
from .set_countdown_times import (
    set_countdown_time 
    )
from .support import (
    clean_text,
    clear_terminal,
    sleep_until_next_loop
    )
from datetime import datetime

def _confirm_hour_format():
    """
    Prompts the user to choose between 12-hour and 24-hour time display formats.
    Repeats until a valid choice is entered.

    Arts: None.
    Returns:
        user_hours (int): The user's preferred time format (12 or 24).
    """
    print("\nWould you like the time to display as 12 hours or 24 hours?")
    print(f'{INDENT}{THIN_HORIZONTAL_LINE}')
    print(f"{INDENT}12 hours looks like this: 3:52pm")
    print(f"{INDENT}24 hours looks like this: 15:52")
    print(f'{INDENT}{THIN_HORIZONTAL_LINE}')

    while True:
        user_input = clean_text(input('Type \"12\" for 12-hour format, or \"24\" for 24-hour format: '))
        try:
            user_hours = int(user_input)
            if user_hours in POSSIBLE_HOUR_DISPLAY_FORMATS:
                return user_hours
            else:
                raise ValueError
        except ValueError:
            print(f"\nError: please enter either 12 or 24. You typed: '{user_input}'\n")

def _format_time(unformatted_time, hour_display_format_from_user):
    """
    Formats a datetime object into a 12-hour or 24-hour time string with timezone.

    Args:
        unformatted_time (datetime): The datetime object to be formatted.
        hours_format_from_user (int): The preferred time format, either 12 or 24.

    Returns:
        formatted_time (str): The formatted time string.
    """
    try:
        hour_display_format_from_user = int(hour_display_format_from_user)
        if hour_display_format_from_user in POSSIBLE_HOUR_DISPLAY_FORMATS:
            timezone = unformatted_time.astimezone().strftime('%Z')
            if hour_display_format_from_user == 12:
                formatted_hours = unformatted_time.strftime('%I:%M')
                formatted_ampm = unformatted_time.strftime('%p').lower()
                formatted_time = f'{formatted_hours}{formatted_ampm} {timezone}'
            elif hour_display_format_from_user == 24:
                formatted_hours = unformatted_time.strftime('%H:%M')
                formatted_time = f'{formatted_hours} {timezone}'
            return formatted_time
        else:
            raise ValueError
    except ValueError:
        print('Hours format must be either \"12\" for 12-hour format, or \"24\" for 24-hour format.')

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
        hour_display_format = _confirm_hour_format()
        
        while True:

            clear_terminal()

            datetime_now = datetime.now().astimezone()
            
            current_date = datetime_now.strftime('%B %d, %Y')
            current_time = _format_time(datetime_now, hour_display_format)
            
            end_of_current_loop = next_occurrence(countdown_times, datetime_now)
            end_of_current_loop_formatted = _format_time(end_of_current_loop, hour_display_format)

            progress_bar_text = progress_bar(total_remaining_seconds(end_of_current_loop, datetime_now))
            remaining_minutes, remaining_seconds = divmod(total_remaining_seconds(end_of_current_loop, datetime_now), 60)

            minutes_label = "minute" if remaining_minutes == 1 else "minutes"
            seconds_label = "second" if remaining_seconds == 1 else "seconds"
    
            print_title_block()

            print(current_date)
            print(f'Current Time: {current_time}')
            
            print('')
            print(THIN_HORIZONTAL_LINE)
            print(f'Countdown until {end_of_current_loop_formatted}:')
            print(THIN_HORIZONTAL_LINE)
            print(f'{INDENT}{remaining_minutes:02} {minutes_label}')
            print(f'{INDENT}{remaining_seconds:02} {seconds_label}')
            print(progress_bar_text)
            
            sleep_until_next_loop()