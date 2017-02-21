/**
* @file test_main.cpp
* @author Dounm <niuchong893184@gmail.com>
* @date 2017-02-17
*/

#include <iostream>
#include <string>
#include "thread_pool.h"

void foo(int x) {
    std::cout << x << std::endl;
}

int main() {
    thread_pool::ThreadPool pool(2);
    pool.start();
    while (1) {
        pool.append(foo);
    }
    return 0;
}
