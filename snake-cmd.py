import curses
from random import randint


class Snake:
    def __init__(self, lines, cols):
        self.cells = [(lines // 2, cols // 2)]
        self.direction = (0, -1)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    curses.curs_set(1)

    stdscr.clear()
    stdscr.addstr(" ____              _        \n"
                  "/ ___| _ __   __ _| | _____ \n"
                  "\\___ \\| '_ \\ / _` | |/ / _ \\\n"
                  " ___) | | | | (_| |   <  __/\n"
                  "|____/|_| |_|\\__,_|_|\\_\\___|\n\n"
                  "Ruben Dougall\n"
                  "2019\n\n"
                  "Press any key to start...")
    stdscr.getch()

    curses.curs_set(0)

    snake = Snake(curses.LINES, curses.COLS)
    pellet = (randint(0, curses.LINES - 1), randint(0, curses.COLS - 1))

    key = None
    game_over = False
    while key != 27 and key != "q" and not game_over:
        stdscr.timeout(1000 // len(snake.cells))
        key = stdscr.getch()

        if key == curses.KEY_LEFT:
            new_direction = (0, -1)
        elif key == curses.KEY_RIGHT:
            new_direction = (0, 1)
        elif key == curses.KEY_UP:
            new_direction = (-1, 0)
        elif key == curses.KEY_DOWN:
            new_direction = (1, 0)
        else:
            new_direction = snake.direction

        new_direction_reversed = (-new_direction[0], -new_direction[1])
        if snake.direction != new_direction_reversed:
            snake.direction = new_direction

        current_front = snake.cells[0]
        # TODO: Use vector library
        new_front = ((current_front[0] + snake.direction[0]) % curses.LINES,
                     (current_front[1] + snake.direction[1]) % curses.COLS)
        snake.cells.insert(0, new_front)

        if pellet in snake.cells:
            pellet = (randint(0, curses.LINES - 1), randint(0, curses.COLS - 1))
        else:
            snake.cells.pop()

        game_over = len(snake.cells) != len(set(snake.cells))

        stdscr.clear()

        stdscr.addstr(0, 0, f"Score: {len(snake.cells)}")

        if len(snake.cells) <= 3:
            stdscr.attron(curses.A_STANDOUT)
            message = "Hint: To move faster, repeatedly press or hold the arrow key."
            stdscr.addstr(0, curses.COLS - len(message), message)
            stdscr.attroff(curses.A_STANDOUT)

        for cell in snake.cells:
            if curses.has_colors():
                stdscr.attron(curses.color_pair(1))
            stdscr.addch(cell[0], cell[1], "x")
            if curses.has_colors():
                stdscr.attroff(curses.color_pair(1))

        if curses.has_colors():
            stdscr.attron(curses.color_pair(2))
        stdscr.addch(pellet[0], pellet[1], "o")
        if curses.has_colors():
            stdscr.attroff(curses.color_pair(2))

    stdscr.nodelay(False)
    curses.curs_set(1)

    stdscr.clear()
    stdscr.addstr("Game over!\n")
    stdscr.addstr(f"Score: {len(snake.cells)}\n\n")
    stdscr.addstr("Press any key to exit...")
    stdscr.getch()

    # TODO: Add some way of displaying controls
    # TODO: For actual game, make window fixed size so you can't cheat by making the terminal window bigger (just don't
    #  use LINES or COLS variables)
    # TODO: Allow option of borders on or off, i.e. to end game or just wrap around (respectively) when snake reaches
    #  edge of the screen
    # TODO: Finish commenting the code


if __name__ == "__main__":
    curses.wrapper(main)
