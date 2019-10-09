#!/usr/bin/env python3
#coding = utf-8

from time import sleep
from threading import Thread, currentThread, Lock, Condition
from abc import ABC, abstractmethod
from src.Statuses import *

'''
class PoolTaskIf
'''
class PoolTaskIf(ABC):
    def __init__(self, strTaskName = ""):
        self.__strTaskName = strTaskName
        self.__threadPool = None
    def __del__(self):
        pass

    def getThreadPool(self):
        return self.__threadPool
    def setThreadPool(self, threadPool):
        self.__threadPool = threadPool
    @abstractmethod
    def run(self):
        pass
    @staticmethod
    def mSleep(ms):
        sleep(ms / 1000)

'''
class PoolThread
'''
class PoolThread(Thread):
    def __init__(self, threadPool):
        super().__init__(target = self.run)
        self.__threadPool = threadPool
        self.__task = None
    def __del__(self):
        if self.__task:
            del self.__task

    def run(self):
        print("[Info]", "PoolThread - enter")
        
        tid = currentThread().ident
        
        while True:
            status, self.__task = self.__threadPool.getTask()
            if status:
                if self.__task:
#                     InfoLog(<<"Thread "<<tid<<" will be busy.");
                    print("[Info]", "Thread {:#x} will be busy.".format(tid))
                    self.__task.run()
                    del self.__task #Delete a task.
#                     InfoLog(<<"Thread "<<tid<<" will be idle.");
                    print("[Info]", "Thread {:#x} will be idle.".format(tid))
            else:
#                 InfoLog(<<"Thread "<<tid<<" will exit.");
                print("[Info]", "Thread {:#x} will exit.".format(tid))
                break
        
        # Remove the binding between the variable self.__threadPool and the object of ThreadPool.
        self.__threadPool = None
        
        print("[Info]", "PoolThread - exit")
        
        return STATUS_OK

'''
class ThreadPool
'''
class ThreadPool:
    def __init__(self, numThreads):
        self.__lThread = list()
        self.__lTask = list()
        self.__shutdown = False
        self.__lock = Lock()
        self.__condition = Condition(self.__lock)
        
        if STATUS_ERR == self.__createAll(numThreads):
            return
        
#         InfoLog(<<numThreads<<" threads are created in this Thread Pool.");
        print("[Info]", "{:d} threads are created in this Thread Pool.".format(numThreads))
    def __del__(self):
        self.shutdownAll()
        self.joinAll()

    def addTask(self, task):
        with self.__lock:
            task.setThreadPool(self)
            self.__lTask.append(task)
            self.__condition.notify()
    def getTask(self):
        with self.__lock:
            while (0 == len(self.__lTask)) and (not self.__shutdown):
                self.__condition.wait()
            
            if self.__shutdown:
                return (False, None)
            
            it = iter(self.__lTask)
            try:
                task = next(it)
                del(self.__lTask[0])
            except StopIteration:
                task = None
            
            return (True, task)
    def shutdownAll(self):
        with self.__lock:
            if not self.__shutdown:
#                 InfoLog(<<"To shutdown all threads in this Thread Pool.");
                print("[Info]", "To shutdown all threads in this Thread Pool.")
                
                self.__shutdown = True
                self.__condition.notify_all()
    def joinAll(self):
        for o in self.__lThread:
            o.join()
            del o
        
        self.__lThread.clear()
    def getPendingTaskNum(self):
        with self.__lock:
            return len(self.__lTask)
    def isShutdown(self):
        with self.__lock:
            return self.__shutdown

    def __createAll(self, numThreads):
        for i in range(numThreads):
            thread = PoolThread(self)
            thread.start()
            self.__lThread.append(thread)
        
        return STATUS_OK

# end of file
