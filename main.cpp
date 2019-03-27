#include <ncurses.h>

using namespace std;

int main()
{
    initscr();

    printw("Hello world!");

    refresh();

    getch();

    endwin();

    return 0;
}
