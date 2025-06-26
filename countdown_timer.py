from datetime import datetime, timedelta
import math
import os
import time
    
def progress_bar(remaining_time_in_seconds):

    """
    Generates a visual progress bar representing the remaining time until the next hour.

    Takes one input, remaining_time_in_seconds (int), which represents the total remaining time in seconds
    until the current timer finishes counting down.

    Each '#' represents about 2 minutes of remaining time. (Every 2 minutes, the '#' character furthest
    to the right is replaced by a '.' character.) The '.' characters represent elapsed time. The
    number of minutes is rounded up if any seconds are left beyond a full minute to ensure a more
    intuitive countdown.

    The bar is 32 characters wide: 30 total '#' and '.' characters, enclosed in a left and right bracket.

    Examples:
    - 16 minutes, 00 seconds → 16 minutes → 8 filled ('#') characters and 22 empty ('.') characters.
    - 16 minutes, 01 second  → 17 minutes → 9 filled ('#') characters and 21 empty ('.') characters.

    Returns:
    str: A string containing the progress bar, e.g. "[##########....................]".
    """

    remaining_minutes_rounded = math.ceil(remaining_time_in_seconds / 60)
    progress_bar_full = '#' * round(remaining_minutes_rounded / 2)
    progress_bar_empty = '.' * (30 - round(remaining_minutes_rounded / 2))
    progress_bar_text = f'[{progress_bar_full}{progress_bar_empty}]'
    return progress_bar_text

def main():

    indent = '  '
    thick_horizontal_line = '=' * 32
    thin_horizontal_line = '-' * 32

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        now = datetime.now().astimezone()

        current_date = now.strftime('%B %d, %Y')
        current_time = now.strftime('%H:%M %Z')

        beginning_of_current_hour = now.replace(minute=0, second=0, microsecond=0)
        beginning_of_next_hour = beginning_of_current_hour + timedelta(hours=1)

        next_loop_begins = beginning_of_next_hour
        next_loop_begins_formatted = next_loop_begins.strftime('%H:%M %Z')

        remaining_time = next_loop_begins - now
        total_remaining_time_in_seconds = int(remaining_time.total_seconds())
        remaining_minutes, remaining_seconds = divmod(total_remaining_time_in_seconds, 60)        

        minutes_label = "minute" if remaining_minutes == 1 else "minutes"
        seconds_label = "second" if remaining_seconds == 1 else "seconds"
  
        print(thick_horizontal_line)
        print('Visual Countdown Timer')
        print('Press Ctrl + C to exit.')
        print(thick_horizontal_line)

        print('')
        print(current_date)
        print(f'Current Time: {current_time}')
        
        print('')
        print(thin_horizontal_line)
        print(f'Countdown until {next_loop_begins_formatted}:')
        print(thin_horizontal_line)
        print(f'{indent}{remaining_minutes:02} {minutes_label}')
        print(f'{indent}{remaining_seconds:02} {seconds_label}')
        print(progress_bar(total_remaining_time_in_seconds))
        
        remaining_time_until_next_loop = 1 - (datetime.now().microsecond / 1_000_000)
        time.sleep(remaining_time_until_next_loop)

if __name__ == '__main__':
    main()