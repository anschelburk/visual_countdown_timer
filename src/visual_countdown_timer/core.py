from . import utils, constants
from datetime import datetime

def main():

    utils.clear_terminal()
    utils.print_title_block(constants.THICK_HORIZONTAL_LINE)
    countdown_end_times = utils.set_countdown_time('initial')
    utils.run_timer()