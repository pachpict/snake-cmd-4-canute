#include <ncurses.h>
#include "Snake.h"
#include <utility>
#include <list>
#include <random>
#include <algorithm>

int positive_modulo(int i, int n);

int random_int(int max);

int main()
{
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    clear();
    addstr("Snake");
    getch();

    Snake snake(COLS, LINES);
    std::pair<int,int> pellet = {random_int(COLS - 1), random_int(LINES - 1)};

    timeout(500);
    int key;
    do {
        key = getch();
        switch (key) {
            case KEY_LEFT:
                snake.direction = {-1, 0};
                break;
            case KEY_RIGHT:
                snake.direction = {1, 0};
                break;
            case KEY_UP:
                snake.direction = {0, -1};
                break;
            case KEY_DOWN:
                snake.direction = {0, 1};
                break;
        }

        std::pair<int,int> current_front = snake.cells.front();
        std::pair<int,int> new_front = {
                positive_modulo(current_front.first + snake.direction.first, COLS),
                positive_modulo(current_front.second + snake.direction.second, LINES)
        };
        snake.cells.push_front(new_front);

        if (std::find(snake.cells.begin(), snake.cells.end(), pellet) != snake.cells.end()) {
            pellet = {random_int(COLS - 1), random_int(LINES - 1)};
        } else {
            snake.cells.pop_back();
        }

        clear();
        mvprintw(0,0,"%d,%d,%d,%d",pellet.first,pellet.second,COLS,LINES);
        for (std::pair<int,int> cell : snake.cells) {
            mvaddch(cell.second, cell.first, 'x');
        }
        mvaddch(pellet.second, pellet.first, 'o');
    } while (key != 27 && key != 'q');

    endwin();

    return 0;
}

// From: https://stackoverflow.com/a/14997413/3806231
int positive_modulo(int i, int n) {
    return (i % n + n) % n;
}

int random_int(int max) {
    static std::random_device rd;
    static std::mt19937 eng(rd());

    std::uniform_int_distribution<> distr(0, max);

    int random_number = distr(eng);
    return random_number;
}
