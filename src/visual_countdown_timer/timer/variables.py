from datetime import datetime, timedelta
import math

def current_date():
    """
    Calculates the current date, formatted as follows: [Month] [Day], [Year].
    Args:
        None.
    Returns:
        current_date (datetime): a datetime object, formatted as described above.
    """
    current_date = datetime.now().strftime('%B %d, %Y')
    return current_date

# def current_time():
#     """
#     Calculates the current time, formatted as follows: [Hour]:[Minute] [Timezone]
#     Args:
#         None.
#     Returns:
#         current_time (datetime): a datetime object, formatted as described above.
#     """
#     current_time = datetime.now().astimezone().strftime('%H:%M %Z')
#     return current_time

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