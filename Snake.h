//
// Created by ruben on 27/03/19.
//

#ifndef SNAKE_CMD_SNAKE_H
#define SNAKE_CMD_SNAKE_H


#include <utility>
#include <list>

class Snake {
private:
    int cols;
    int lines;
public:
    Snake(int cols, int lines);

    std::list<std::pair<int, int>> cells = {{cols / 2, lines / 2}};
    std::pair<int, int> direction = {0, -1};
};


#endif //SNAKE_CMD_SNAKE_H
