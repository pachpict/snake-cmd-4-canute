#include <ncurses.h>
#include "Snake.h"

int main()
{
    initscr();

    clear();
    addstr("Snake");
    getch();

    clear();
    Snake snake(LINES, COLS);
    for (auto cell : snake.cells) {
        mvaddch(cell.first,cell.second,'x');
    }
    getch();

    endwin();

    return 0;
}
