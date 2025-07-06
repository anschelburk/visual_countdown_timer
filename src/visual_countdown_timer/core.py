from . import utils, constants
from datetime import datetime

def main():

    utils.clear_terminal()
    utils.print_title_block(constants.THICK_HORIZONTAL_LINE)
    countdown_end_times = utils.set_countdown_time('initial')

    while True:

        utils.clear_terminal()

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
  
        utils.print_title_block(constants.THICK_HORIZONTAL_LINE)

        print(current_date)
        print(f'Current Time: {current_time}')
        
        print('')
        print(constants.THIN_HORIZONTAL_LINE)
        print(f'Countdown until {end_of_current_loop_formatted}:')
        print(constants.THIN_HORIZONTAL_LINE)
        print(f'{constants.INDENT}{remaining_minutes:02} {minutes_label}')
        print(f'{constants.INDENT}{remaining_seconds:02} {seconds_label}')
        print(utils.progress_bar(total_remaining_time_in_seconds))
        
        utils.sleep_until_next_loop()