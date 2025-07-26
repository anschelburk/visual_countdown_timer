from .constants import INDENT, THICK_HORIZONTAL_LINE, THIN_HORIZONTAL_LINE
from .timer_logic import TimerLogic             # [x] Confirmed
from .timer_display import TimerDisplay         # [x] Confirmed, but consider making two classes: DisplayLogic (for __init__) and DisplayText (for things like print_title_block())
from .timer_input import UserInput              # [x] Confirmed
from .timer_utils import SupportUtils           # [x] Confirmed
from .timer_settings import TimerConfig         # [x] Confirmed
from .support import clear_terminal, sleep_until_next_loop
from datetime import datetime

class TimerApp:
    """Main timer application class that coordinates all components."""
    
    def __init__(self):
        self.timer_logic = TimerLogic()               # [x] Confirmed
        self.display = TimerDisplay()                 # [x] Confirmed
        self.user_input = UserInput()                 # [x] Confirmed
        SupportUtils.initialize_exit_handler()        # [x] Confirmed
    
    def print_title_block(self):
        """Prints the title block for the Visual Countdown Timer interface."""
        print(THICK_HORIZONTAL_LINE)
        print('Visual Countdown Timer')
        print('Press Ctrl + C to exit.')
        print(f'{THICK_HORIZONTAL_LINE}\n')
    
    def run(self):
        """Main application entry point."""
        clear_terminal()
        self.print_title_block()
        
        # Get initial configuration
        countdown_minutes = self.user_input.get_countdown_time('initial')
        hour_format = self.user_input.get_hour_format()
        
        # Run the timer loop
        self._timer_loop(countdown_minutes, hour_format)
    
    def _timer_loop(self, countdown_minutes: int, hour_format: int):
        """
        Main timer loop that displays countdown information.
        
        Args:
            countdown_minutes: Target minute past each hour
            hour_format: 12 or 24 hour format preference
        """
        while True:
            clear_terminal()
            
            current_time = datetime.now().astimezone()
            target_time = self.timer_logic.get_next_occurrence(countdown_minutes, current_time)
            remaining_seconds = self.timer_logic.get_remaining_seconds(target_time, current_time)
            
            # Display current information
            self.print_title_block()
            self.display.show_current_info(current_time, hour_format)
            self.display.show_countdown_info(target_time, remaining_seconds, hour_format)
            
            sleep_until_next_loop()
