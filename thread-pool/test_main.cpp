/**
* @file test_main.cpp
* @author Dounm <niuchong893184@gmail.com>
* @date 2017-02-17
*/

#include "thread_pool.h"
#include <iostream>
#include <string>

void foo() {
    std::cout << "foo" << std::endl;
}

void bar(const std::string& str) {
    std::cout << str << std::endl;
}

int main() {
    thread_pool::ThreadPool pool(10);
    pool.append(foo);
    pool.append(std::bind(&bar, "bar"));
    pool.append(foo);
    pool.start();
    std::cout << "done" << std::endl;
    pool.stop();
    return 0;
}
