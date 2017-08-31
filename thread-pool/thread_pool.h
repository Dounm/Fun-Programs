/**
* @file thread_pool.h
* @author Dounm <niuchong893184@gmail.com>
* @date 2017-02-17
*/

#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#define DISALLOW_COPY_AND_ASSIGN(TypeName) \
            TypeName(const TypeName&); \
            TypeName& operator=(const TypeName&) 

#include <string>
#include <vector>
#include <memory>
#include <list>
#include <functional>
#include <thread>
#include <mutex>
#include <condition_variable>

namespace thread_pool {

class ThreadPool {
public:
    typedef std::function<void()> Task;
    ThreadPool(int thread_num) : _mutex(),
                            _condition_empty(),
                            _tasks(),
                            _running(true),
                            _thread_num(thread_num),
                            _threads() { }
    ~ThreadPool();
    
    void start();
    void stop();
    void append(Task task);

private:
    DISALLOW_COPY_AND_ASSIGN(ThreadPool);

    void work();

    std::mutex _mutex;
    std::condition_variable_any _condition_empty;
    std::list<Task> _tasks;
    bool _running;
    size_t _thread_num;
    std::vector<std::shared_ptr<std::thread> > _threads; 
};
    
}

#endif
