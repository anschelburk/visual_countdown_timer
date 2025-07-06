from . import utils
from datetime import datetime
import os
import time

def main():

    os.system('cls' if os.name == 'nt' else 'clear')

    indent = '  '
    thick_horizontal_line = '=' * 32
    thin_horizontal_line = '-' * 32

    print(thick_horizontal_line)
    print('Visual Countdown Timer')
    print('Press Ctrl + C to exit.')
    print(thick_horizontal_line)

    print('')
    countdown_end_times = utils.set_countdown_time('initial')

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        now = datetime.now().astimezone()

        current_date = now.strftime('%B %d, %Y')
        current_time = now.strftime('%H:%M %Z')
        
        end_of_current_loop = utils.next_occurrence(now, countdown_end_times)
        end_of_current_loop_formatted = end_of_current_loop.strftime('%H:%M %Z')

        remaining_time = end_of_current_loop - now
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
        print(f'Countdown until {end_of_current_loop_formatted}:')
        print(thin_horizontal_line)
        print(f'{indent}{remaining_minutes:02} {minutes_label}')
        print(f'{indent}{remaining_seconds:02} {seconds_label}')
        print(utils.progress_bar(total_remaining_time_in_seconds))
        
        remaining_time_until_next_loop = 1 - (datetime.now().microsecond / 1_000_000)
        time.sleep(remaining_time_until_next_loop)