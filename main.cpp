#include <ncurses.h>
#include "Snake.h"

int main()
{
    initscr();
    cbreak();
    noecho();

    clear();
    addstr("Snake");
    getch();

    Snake snake(COLS, LINES);
    timeout(500);
    while (true) {
        std::pair<int,int> current_front = snake.cells.front();
        std::pair<int,int> new_front = {current_front.first + snake.direction.first, current_front.second + snake.direction.second};
        snake.cells.push_front(new_front);

        snake.cells.pop_back();

        clear();
        for (std::pair<int,int> cell : snake.cells) {
            mvaddch(cell.second, cell.first, 'x');
        }
        getch();
    }

    endwin();

    return 0;
}
