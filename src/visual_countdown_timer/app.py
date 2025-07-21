from .timer.actions import (
    print_title_block,
    run_timer
    )

from .timer.support import clear_terminal

def main():
    clear_terminal()
    print_title_block()
    run_timer()