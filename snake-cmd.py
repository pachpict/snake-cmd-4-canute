import curses
import vectormath as vm


class Snake:
    def __init__(self):
        self.cells = [vm.Vector2(curses.LINES // 2, curses.COLS // 2)]
        self.direction = vm.Vector2(0, -1)

def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.box()

    stdscr.addstr(0, 0, "Snake")

    stdscr.refresh()
    stdscr.getkey()

    stdscr.clear()

    snake = Snake()
    for cell in snake.cells:
        stdscr.addstr(int(cell.x), int(cell.y), "x")

    stdscr.refresh()
    stdscr.getkey()


curses.wrapper(main)
