#include <ncurses.h>

using namespace std;

int main()
{
    initscr();

    clear();
    addstr("Snake");
    refresh();
    getch();

    endwin();

    return 0;
}
