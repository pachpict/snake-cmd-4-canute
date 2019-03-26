import curses
import vectormath as vm
import threading


class Snake:
    def __init__(self):
        self.cells = [vm.Vector2(curses.LINES // 2, curses.COLS // 2)]
        self.direction = vm.Vector2(0, -1)

    def move(self):
        for cell in self.cells:
            cell += self.direction


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return


def main(stdscr):
    # Clear screen
    stdscr.clear()

    stdscr.box()

    stdscr.addstr(0, 0, "Snake")

    stdscr.refresh()
    stdscr.getkey()

    snake = Snake()

    def update():
        snake.move()

        stdscr.clear()

        for cell in snake.cells:
            stdscr.addstr(int(cell.x), int(cell.y), "x")

        stdscr.refresh()
        # stdscr.getkey()

    set_interval(update, 0.5)

curses.wrapper(main)
