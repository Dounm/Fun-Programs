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
        for (const auto& thread : _threads) {
            thread->join();
        }
    }
}

void ThreadPool::append(Task task) {
    std::lock_guard<std::mutex> guard(_mutex);
    _tasks.push_front(task);
    _condition_empty.notify_one();    // wake one(not sure which one) thread to handle the task
}

void ThreadPool::work() {
    Task task = nullptr;
    int cnt = 0;
    while (_running) {
        {
            std::unique_lock<std::mutex> guard(_mutex);
            // TODO: why this won't work
            // if (_tasks.empty()) {
            //     _condition_empty.wait(_mutex);
            // }
            // task = _tasks.front();
            // _tasks.pop_front();
            if (_tasks.empty()) {
                _condition_empty.wait(_mutex);
            } 
            if (!_tasks.empty()) {
                task = _tasks.front();
                _tasks.pop_front();
            }else {
                cnt ++;
                continue;
            }
        }           // braces are for unlocking _mutex
        task(cnt);
    }
}

}
