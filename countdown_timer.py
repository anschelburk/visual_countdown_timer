from datetime import datetime, timedelta
import math
import os
import time

def main():

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        now = datetime.now().astimezone()

        current_date = now.strftime('%B %d, %Y')
        current_time = now.strftime('%H:%M %Z')

        beginning_of_current_hour = now.replace(minute=0, second=0, microsecond=0)
        beginning_of_next_hour = beginning_of_current_hour + timedelta(hours=1)

        remaining_time = beginning_of_next_hour - now
        total_remaining_time_in_seconds = int(remaining_time.total_seconds())
        remaining_minutes, remaining_seconds = divmod(total_remaining_time_in_seconds, 60)        

        # For progress bar, calculate number of remaining minutes, rounding up if any seconds are left.
        # Store this value in a new variable, remaining_minutes_rounded.
        # Example:  16 min : 01 sec  -->  17 min
        # Example:  16 min : 00 sec  -->  16 min
        remaining_minutes_rounded = math.ceil(total_remaining_time_in_seconds / 60)

        progress_bar_full = '#' * round(remaining_minutes_rounded / 2)
        progress_bar_empty = '.' * (30 - round(remaining_minutes_rounded / 2))
        progress_bar = f'[{progress_bar_full}{progress_bar_empty}]'

        minutes_label = "minute" if remaining_minutes == 1 else "minutes"
        seconds_label = "second" if remaining_seconds == 1 else "seconds"

        thick_horizontal_line = '=' * 32
        thin_horizontal_line = '-' * 32
        
        print(thick_horizontal_line)
        print('Hourly Countdown Timer')
        print('Press Ctrl + C to exit.')
        print(thick_horizontal_line)

        print('')
        print(f'{current_date}')
        print(f'Current Time: {current_time}')
        
        print('')
        print(thin_horizontal_line)
        print(f'Countdown until {beginning_of_next_hour.strftime("%H:%M %Z")}:')
        print(thin_horizontal_line)
        print(f'  {remaining_minutes:02} {minutes_label}')
        print(f'  {remaining_seconds:02} {seconds_label}')
        print(progress_bar)
        
        remaining_time_until_next_refresh = 1 - (datetime.now().microsecond / 1_000_000)
        time.sleep(remaining_time_until_next_refresh)

if __name__ == '__main__':
    main()