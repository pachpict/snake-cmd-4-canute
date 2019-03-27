#include <ncurses.h>
#include "Snake.h"

int main()
{
    initscr();

    clear();
    addstr("Snake");
    refresh();

    Snake snake(LINES, COLS);
    printw(",%d,%d",snake.cells.front().first,snake.cells.front().second);
    getch();

    endwin();

    return 0;
}
