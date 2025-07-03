from datetime import datetime, timedelta
import math
import os
import time

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

        user_input = input(f'Please enter the{_new} number of minutes you\'d like to count down to: ')
        
        try:
            user_minutes = int(user_input)    
            if 0 <= user_minutes < 60:
                print(f'\nYou entered {user_minutes} minutes. The timer will count down to:')
                print(f'1:{user_minutes} | 2:{user_minutes} | 3:{user_minutes} | etc.\n')
                confirmation = input('Please confirm your selection (y/n): ').lower()
                while confirmation != 'y':
                    if confirmation == 'n':
                        print('')
                        break
                    else:
                        print('\nPlease enter \"y\" for yes, or \"n\" for no.\n')
                        confirmation = input('Is this correct? Please enter \'y\' or \'n\': ').lower()
                if confirmation == 'y':
                    break
            else:
                print("\nError: Please enter a number of minutes between 0 and 59.")
                print('')

        except ValueError:
            print("\nError: Please enter a valid number (e.g., 25).")
            print("This number must be written as an integer. \"3\" works; \"three\" doesn't.")
            print('')

    return user_minutes

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
    countdown_end_times = set_countdown_time('initial')

    while True:

        os.system('cls' if os.name == 'nt' else 'clear')

        now = datetime.now().astimezone()

        current_date = now.strftime('%B %d, %Y')
        current_time = now.strftime('%H:%M %Z')
        
        end_of_current_loop = next_occurrence(now, countdown_end_times)
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
        print(progress_bar(total_remaining_time_in_seconds))
        
        remaining_time_until_next_loop = 1 - (datetime.now().microsecond / 1_000_000)
        time.sleep(remaining_time_until_next_loop)

if __name__ == '__main__':
    main()