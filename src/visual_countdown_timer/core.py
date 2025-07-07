from . import utils, constants

def main():
    utils.clear_terminal()
    utils.print_title_block(constants.THICK_HORIZONTAL_LINE)
    countdown_end_times = utils.set_countdown_time('initial')
    utils.run_timer(
        countdown_times = countdown_end_times,
        thick_line = constants.THICK_HORIZONTAL_LINE,
        thin_line = constants.THIN_HORIZONTAL_LINE,
        indent = constants.INDENT
        )