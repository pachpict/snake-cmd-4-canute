//
// Created by ruben on 27/03/19.
//

#ifndef SNAKE_CMD_SNAKE_H
#define SNAKE_CMD_SNAKE_H


#include <utility>
#include <list>

class Snake {
private:
    int lines;
    int cols;
public:
    Snake(int lines, int cols);

    std::list<std::pair<int, int>> cells = {{lines / 2, cols / 2}};
};


#endif //SNAKE_CMD_SNAKE_H
