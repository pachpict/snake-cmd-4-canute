import curses
from random import randint


class Snake:
    def __init__(self, lines, cols):
        self.cells = [(lines // 2, cols // 2)]
        self.direction = (0, -1)


def main(stdscr):
    # Initialise colours
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Show cursor
    curses.curs_set(1)

    stdscr.clear()
    show_title_screen(stdscr)

    # Hide cursor
    curses.curs_set(0)

    score = show_game_screen(stdscr)

    # Show cursor
    curses.curs_set(1)

    # TODO: Refactor this into separate method too
    stdscr.clear()
    stdscr.addstr("Game over!\n")
    stdscr.addstr(f"Score: {score}\n\n")
    stdscr.addstr("Press any key to exit...")
    stdscr.getch()

    # TODO: Add some way of displaying controls
    # TODO: For actual game, make window fixed size so you can't cheat by making the terminal window bigger (just don't
    #  use LINES or COLS variables)
    # TODO: Allow option of borders on or off, i.e. to end game or just wrap around (respectively) when snake reaches
    #  edge of the screen
    # TODO: Refactor screens into separate classes (?)
    # TODO: Fix error when resizing window during playing (?)


def show_title_screen(stdscr):
    stdscr.addstr(" ____              _        \n"
                  "/ ___| _ __   __ _| | _____ \n"
                  "\\___ \\| '_ \\ / _` | |/ / _ \\\n"
                  " ___) | | | | (_| |   <  __/\n"
                  "|____/|_| |_|\\__,_|_|\\_\\___|\n\n"
                  "Ruben Dougall\n"
                  "2019\n\n"
                  "Press any key to start...")
    stdscr.getch()


def show_game_screen(stdscr):
    snake = Snake(stdscr.getmaxyx()[0], stdscr.getmaxyx()[1])
    pellet = (randint(0, stdscr.getmaxyx()[0] - 1), randint(0, stdscr.getmaxyx()[1] - 1))

    key = None
    # getch return value of 27 corresponds to escape key - doesn't look like curses has a constant for this
    # 3rd condition checks if snake has "eaten" (intersected with) itself, i.e. whether any cells re-appear in the list
    while key != 27 and key != ord("q") and len(snake.cells) == len(set(snake.cells)):
        # Set the maximum amount of time to block for a key press
        # This is effectively the update interval
        stdscr.timeout(1000 // len(snake.cells))
        key = stdscr.getch()

        # Update
        pellet = update_game_screen(stdscr, key, snake, pellet)

        # Draw
        draw_game_screen(stdscr, snake, pellet)

    # For user input, remove the timeout but keep blocking enabled
    stdscr.nodelay(False)

    # Return score
    return len(snake.cells)


def update_game_screen(stdscr, key, snake, pellet):
    # Set new direction based on the key input
    # If an arrow key wasn't pressed then continue in same direction
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

    # Prevent the snake reversing on itself, i.e. check that the snake's current and new directions aren't the reverse
    # of one another
    new_direction_reversed = (-new_direction[0], -new_direction[1])
    if snake.direction != new_direction_reversed:
        snake.direction = new_direction

    #
    current_front = snake.cells[0]
    # TODO: Use vector library
    new_front = ((current_front[0] + snake.direction[0]) % stdscr.getmaxyx()[0],
                 (current_front[1] + snake.direction[1]) % stdscr.getmaxyx()[1])
    snake.cells.insert(0, new_front)

    # If the snake just "ate" (intersected with) a pellet:
    # * Effectively increase the length by 1, by not removing a cell to compensate for the one just added
    # * Move the pellet to a random position
    # If the snake didn't just "eat" a pellet:
    # * Remove a cell to compensate for the one just added, so length of the snake stays the same
    # * Obviously leave the pellet where it is
    if pellet in snake.cells:
        pellet = (randint(0, stdscr.getmaxyx()[0] - 1), randint(0, stdscr.getmaxyx()[1] - 1))
    else:
        snake.cells.pop()

    # Return pellet so changes are reflected in the caller
    # Don't need to return snake as it's only modified, not written to
    return pellet


def draw_game_screen(stdscr, snake, pellet):
    stdscr.clear()

    # Display score
    stdscr.addstr(0, 0, f"Score: {len(snake.cells)}")

    # Display hint
    if len(snake.cells) <= 3:
        stdscr.attron(curses.A_STANDOUT)
        message = "Hint: To move faster, repeatedly press or hold the arrow key."
        stdscr.addstr(0, stdscr.getmaxyx()[1] - len(message), message)
        stdscr.attroff(curses.A_STANDOUT)

    # Draw snake
    for cell in snake.cells:
        if curses.has_colors():
            stdscr.attron(curses.color_pair(1))
        stdscr.addch(cell[0], cell[1], "x")
        if curses.has_colors():
            stdscr.attroff(curses.color_pair(1))

    # Draw pellet
    if curses.has_colors():
        stdscr.attron(curses.color_pair(2))
    stdscr.addch(pellet[0], pellet[1], "o")
    if curses.has_colors():
        stdscr.attroff(curses.color_pair(2))


if __name__ == "__main__":
    curses.wrapper(main)
