import curses


def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.box()

    stdscr.addstr(0, 0, "Snake")

    stdscr.refresh()
    stdscr.getkey()


curses.wrapper(main)
