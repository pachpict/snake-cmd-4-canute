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
    curs_set(1);

    bool use_color = has_colors();
    if (use_color) {
        start_color();
    }
    init_pair(1, COLOR_CYAN, COLOR_BLACK); // Colour pair for snake
    init_pair(2, COLOR_YELLOW, COLOR_BLACK); // Colour pair for pellets

    clear();
    addstr(" ____              _        \n"
           "/ ___| _ __   __ _| | _____ \n"
           "\\___ \\| '_ \\ / _` | |/ / _ \\\n"
           " ___) | | | | (_| |   <  __/\n"
           "|____/|_| |_|\\__,_|_|\\_\\___|\n\n"
           "Ruben Dougall\n"
           "2019\n\n"
           "Press any key to start...");
    getch();

    curs_set(0);

    Snake snake(COLS, LINES);
    std::pair<int,int> pellet = {random_int(COLS - 1), random_int(LINES - 1)};

    int key;
    bool game_over;
    do {
        timeout(1000 / snake.cells.size());

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
            default:
                break;
        }

        std::pair<int,int> current_front = snake.cells.front();
        std::pair<int,int> new_front = {
                positive_modulo(current_front.first + snake.direction.first, COLS),
                positive_modulo(current_front.second + snake.direction.second, LINES)
        };
        snake.cells.push_front(new_front);

        auto find_pellet_it = std::find(snake.cells.begin(), snake.cells.end(), pellet);
        if (find_pellet_it != snake.cells.end()) {
            pellet = {random_int(COLS - 1), random_int(LINES - 1)};
        } else {
            snake.cells.pop_back();
        }

        // Game over if snake eats itself
        // Specifically, this is if the snake cells list contains one or more duplicates
        std::list<std::pair<int, int>> cells_copy = snake.cells;
        cells_copy.sort();
        auto unique_it = std::unique(cells_copy.begin(), cells_copy.end());
        game_over = (unique_it != cells_copy.end());

        clear();
        mvprintw(0, 0, "Score: %d", snake.cells.size()); // TODO: Might move these to separate window later
        if (snake.cells.size() <= 3) {
            attron(A_STANDOUT);
            std::string message = "Hint: to move faster, press the arrow keys repeatedly.";
            mvprintw(0, COLS - message.length(), message.c_str());
            attroff(A_STANDOUT);
        }
        for (std::pair<int,int> cell : snake.cells) {
            if (use_color) {
                attron(COLOR_PAIR(1));
            }
            mvaddch(cell.second, cell.first, 'x');
            if (use_color) {
                attroff(COLOR_PAIR(1));
            }
        }
        if (use_color) {
            attron(COLOR_PAIR(2));
        }
        mvaddch(pellet.second, pellet.first, 'o');
        if (use_color) {
            attroff(COLOR_PAIR(2));
        }
    } while (key != 27 && key != 'q' && !game_over);

    nodelay(stdscr, FALSE);

    curs_set(1);

    clear();
    printw("Game over!\n");
    printw("Score: %d\n\n", snake.cells.size());
    printw("Press any key to exit");
    getch();

    // TODO: Add some way of displaying controls
    // TODO: For actual game, make window fixed size so you can't cheat by making the terminal window bigger
    // TODO: Prevent snake going back on itself

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
