import curses
from random import randint
from enum import Enum, auto


class Snake:
    def __init__(self, lines, cols):
        self.cells = [(lines // 2, cols // 2)]
        self.direction = (-1, 0)


class HorizontalAlignment(Enum):
    LEFT = auto()
    CENTER = auto()
    RIGHT = auto()


def main(stdscr):
    # Initialise colours
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Show cursor
    curses.curs_set(1)

    show_title_screen(stdscr)

    # Hide cursor
    curses.curs_set(0)

    score = show_game_screen(stdscr)

    # Show cursor
    curses.curs_set(1)

    show_game_over_screen(stdscr, score)

    # TODO: Add some way of displaying controls
    # TODO: For actual game, make window fixed size so you can't cheat by making the terminal window bigger (just don't
    #  use LINES or COLS variables)
    # TODO: Allow option of borders on or off, i.e. to end game or just wrap around (respectively) when snake reaches
    #  edge of the screen
    # TODO: Refactor screens into separate classes (?)
    # TODO: Fix error when resizing window during playing (?)


def show_title_screen(stdscr):
    stdscr.clear()

    y = 0
    y += addstr_multiline_aligned(stdscr, y, " ____              _        \n"
                           "/ ___| _ __   __ _| | _____ \n"
                           "\\___ \\| '_ \\ / _` | |/ / _ \\\n"
                           " ___) | | | | (_| |   <  __/\n"
                           "|____/|_| |_|\\__,_|_|\\_\\___|\n", HorizontalAlignment.CENTER)
    y += addstr_multiline_aligned(stdscr, y, "Ruben Dougall", HorizontalAlignment.CENTER)
    y += addstr_multiline_aligned(stdscr, y, "2019\n", HorizontalAlignment.CENTER)
    y += addstr_multiline_aligned(stdscr, y, "Press any key to start...", HorizontalAlignment.CENTER)
    stdscr.getch()


def addstr_multiline_aligned(stdscr, y, text, alignment=HorizontalAlignment.LEFT):
    return addstr_multiline(stdscr, y, align_text(stdscr, text, alignment), text)


# Passing a multi-line string and a position to addstr will mean that the first line begins at that position but the
# following lines will start at the 0th column
# This function prints the text so the lines are horizontally aligned
def addstr_multiline(stdscr, y, x, text):
    lines = text.split("\n")
    for line in lines:
        stdscr.addstr(y, x, line)
        y += 1

    return len(lines)


# Calculates column the text should start at (i.e. the argument x for the addstr method) when aligned using the given
# alignment
def align_text(stdscr, text, alignment):
    window_width = stdscr.getmaxyx()[1]
    window_left = stdscr.getbegyx()[1]

    # The input text may contain multiple lines
    # The overall width of the text is the length of the longest line
    lines = text.split("\n")
    text_width = max(map(len, lines))

    if alignment == HorizontalAlignment.RIGHT:
        window_right = window_left + window_width - 1
        text_left = window_right - text_width + 1
    elif alignment == HorizontalAlignment.CENTER:
        text_left = window_left + ((window_width - text_width) // 2)
    else:
        text_left = 0

    return text_left


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

    # Display score
    stdscr.addstr(0, 0, f"Score: {len(snake.cells)}")

    # Display hint
    if len(snake.cells) <= 3:
        stdscr.attron(curses.A_STANDOUT)
        message = "Hint: To move faster, repeatedly press or hold the arrow key."
        stdscr.addstr(0, stdscr.getmaxyx()[1] - len(message), message)
        stdscr.attroff(curses.A_STANDOUT)


def show_game_over_screen(stdscr, score):
    stdscr.clear()

    y = 0
    y += addstr_multiline_aligned(stdscr, y, "Game over!\n", HorizontalAlignment.CENTER)
    y += addstr_multiline_aligned(stdscr, y, f"Score: {score}\n\n", HorizontalAlignment.CENTER)
    y += addstr_multiline_aligned(stdscr, y, "Press any key to exit...", HorizontalAlignment.CENTER)

    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
