#!/usr/bin/env python3
#coding = utf-8

from socket import *
from threading import Thread, Lock, Condition
from src.Constants import *
from src.Statuses import *
from src.IpAddr import *
from src.ThreadPool import ThreadPool
from src.TcpServerConnTask import TcpServerConnTask

TCP_SERVER_THREAD_BUFFER_LENGTH = (1 * 1024 * 1024) # 1 MB

'''
class TcpServerListenThread
'''
class TcpServerListenThread(Thread):
    def __init__(self, ipVer, strLocalIpAddr, localPortNumber):
        super().__init__(target = self.run)
        self.__ipVer = ipVer
        self.__strLocalIpAddr = strLocalIpAddr
        self.__localPortNumber = localPortNumber
        self.__shutdown = False
        self.__lock = Lock()
        self.__condition = Condition(self.__lock)
    def __del__(self):
        pass

    def run(self):
        print("[Info]", "TcpServerListenThread - enter")
        
        threadPool = ThreadPool(THREAD_POOL_NUM_THREADS)
        
        # Open a TCP Server Socket for listening.
        listenTcpServerSockFd = socket(AF_INET if IP_ADDR_VER_4 == self.__ipVer else AF_INET6, \
                                              SOCK_STREAM)
        if STATUS_ERR == listenTcpServerSockFd:
#             ErrLog(<<"Fail to open a TCP Server Socket for listening!");
            print("[Err]", "Fail to open a TCP Server Socket for listening!")
            return STATUS_ERR
        
        # Non-blocking I/O
        listenTcpServerSockFd.setblocking(False)
        
        # Configure a TCP Server Socket for listening with addr and port.
        ret = listenTcpServerSockFd.bind((self.__strLocalIpAddr, self.__localPortNumber))
        if STATUS_ERR == ret:
#             ErrLog(<<"Fail to configure a TCP Server Socket for listening with addr and port!");
            print("[Err]", "Fail to configure a TCP Server Socket for listening with addr and port!")
            return STATUS_ERR
        
        # Transfer to Listen state on TCP server.
        ret = listenTcpServerSockFd.listen(TCP_CONNECTIONS_MAX_NUM)
        if STATUS_ERR == ret:
#             ErrLog(<<"Fail to transfer to Listen state on TCP server!");
            print("[Err]", "Fail to transfer to Listen state on TCP server!")
            return STATUS_ERR
        
        while not self.__waitForShutdown(10): # Wait for 10 ms.
            while True:
                try:
                    # Accept TCP client.
                    connTcpServerSockFd, addr = listenTcpServerSockFd.accept()
                except BlockingIOError:
                    # No new TCP connection.
                    break
                else:
                    # A new TCP connection.
                    # Create a TCP Server Connection Task.
                    task = TcpServerConnTask(connTcpServerSockFd)
                    
                    # Add a TCP Server Connection Task to the Thread Pool.
                    threadPool.addTask(task)
#                     InfoLog(<<"Add a TCP Server Connection Task to the Thread Pool.");
                    print("[Info]", "Add a TCP Server Connection Task to the Thread Pool.")
                    
                    # Remove the binding between the variable task and the object of TcpServerConnTask.
                    del task
        
        # Close the TCP Server Socket for listening.
        listenTcpServerSockFd.close()
#         InfoLog(<<"Close the TCP Server Socket for listening.");
        print("[Info]", "Close the TCP Server Socket for listening.")
        
        # Shutdown all threads in the Thread Pool.
        threadPool.shutdownAll()
        threadPool.joinAll()
        
        print("[Info]", "TcpServerListenThread - exit")
        
        return STATUS_OK
    def shutdown(self):
        with self.__lock:
            if not self.__shutdown:
                self.__shutdown = True
                self.__condition.notify()
    def isShutdown(self):
        with self.__lock:
            return self.__shutdown

    def __waitForShutdown(self, ms):
        with self.__lock:
            if not self.__shutdown:
                self.__condition.wait(ms / 1000)
            return self.__shutdown

# end of file
