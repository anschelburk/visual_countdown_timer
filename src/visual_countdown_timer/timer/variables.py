from datetime import datetime, timedelta
import math

current_date = datetime.now().strftime('%B %d, %Y')
datetime_now = datetime.now().astimezone()

def next_occurrence(target_minute):
    """
    Returns the next datetime where the minute equals target_minute.

    Args:
        target_minute (int): The target minute after the hour that the timer should count down to.

    Returns:
        next_occurrence (datetime): The next datetime where the minute equals target_minute.
    """
    # If the target minute has not yet passed for the current hour:
    if datetime_now.minute < target_minute:
        next_occurrence = datetime_now.replace(minute=target_minute, second=0, microsecond=0)
    
    # If the target minute has already passed for the current hour:
    else:
        next_hour = datetime_now + timedelta(hours=1)
        next_occurrence = next_hour.replace(minute=target_minute, second=0, microsecond=0)
    
    return next_occurrence

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

# Not in use yet.
def time_label(remaining_time, minutes_or_seconds):
    if minutes_or_seconds == 'minutes':
        time_label = 'minute' if remaining_time == 1 else 'minutes'
    elif minutes_or_seconds == 'seconds':
        time_label = 'second' if remaining_time == 1 else 'seconds'
    else:
        time_label = 'Error: invalid input for time_label() function.'
    return time_label

def total_remaining_time_in_seconds(end_of_current_timer_loop):
    remaining_time = end_of_current_timer_loop - datetime_now
    total_remaining_time_in_seconds = int(remaining_time.total_seconds())
    return total_remaining_time_in_seconds