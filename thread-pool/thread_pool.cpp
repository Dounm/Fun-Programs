/**
* @file thread_pool.cpp
* @author Dounm <niuchong893184@gmail.com>
* @date 2017-02-17
*/

#include "thread_pool.h"

namespace thread_pool {

ThreadPool::~ThreadPool() {
    if (_running) {
        stop();
    }
}

void ThreadPool::start() {
    for (size_t i = 0; i < _thread_num; ++i) {
        _threads.push_back(std::make_shared<std::thread>(std::bind(&ThreadPool::work, this)));
    }
}

void ThreadPool::stop() {
    if (_running) {
        _running = false;
        _condition_empty.notify_all();
        for (const auto& thread : _threads) {
            thread->join();
        }
    }
}

void ThreadPool::append(Task task) {
    std::lock_guard<std::mutex> guard(_mutex);
    _tasks.push_front(task);
    _condition_empty.notify_one();    // wake one(not sure which one) thread to handle the task
    // when all threads are awake, this line is no use. 
    // and the awake threads will consume all tasks until the list is empty, then go to sleep
}

void ThreadPool::work() {
    Task task = nullptr;
    while (_running) {
        {
            std::unique_lock<std::mutex> guard(_mutex);
            if (_tasks.empty()) {
                // _condition_empty.wait(_mutex);   // not mutex but lock
                // this line still could be compiled, but _condition_empty is waitint on a new lock obj
                _condition_empty.wait(guard);
            }
            if (!_tasks.empty()) {           // judge if notified by notify_all() or notify_one()
                task = _tasks.front();
                _tasks.pop_front();
            } else {
                continue;
            }
        }           // braces are for unlocking _mutex
        task();  // run task when _mutex is unlocked
    }
}

}
