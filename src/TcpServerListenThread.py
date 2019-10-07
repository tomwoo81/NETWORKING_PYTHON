#!/usr/bin/env python3
#coding = utf-8

from socket import *
from threading import Thread
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
        self.__threadPool = ThreadPool(THREAD_POOL_NUM_THREADS)
    def __del__(self):
        if self.__threadPool:
            del self.__threadPool
            self.__threadPool = None

    def run(self):
        print("[Info]", "TcpServerListenThread - enter")
        
        # Open a TCP Server Socket for listening.
        self.__listenTcpServerSockFd = socket(AF_INET if IP_ADDR_VER_4 == self.__ipVer else AF_INET6, \
                                              SOCK_STREAM) # blocking I/O
        if STATUS_ERR == self.__listenTcpServerSockFd:
#             ErrLog(<<"Fail to open a TCP Server Socket for listening!");
            print("[Err]", "Fail to open a TCP Server Socket for listening!")
            return STATUS_ERR
        
        # Configure a TCP Server Socket for listening with addr and port.
        ret = self.__listenTcpServerSockFd.bind((self.__strLocalIpAddr, self.__localPortNumber))
        if STATUS_ERR == ret:
#             ErrLog(<<"Fail to configure a TCP Server Socket for listening with addr and port!");
            print("[Err]", "Fail to configure a TCP Server Socket for listening with addr and port!")
            return STATUS_ERR
        
        # Transfer to Listen state on TCP server.
        ret = self.__listenTcpServerSockFd.listen(TCP_CONNECTIONS_MAX_NUM)
        if STATUS_ERR == ret:
#             ErrLog(<<"Fail to transfer to Listen state on TCP server!");
            print("[Err]", "Fail to transfer to Listen state on TCP server!")
            return STATUS_ERR
        
        while True:
            # Accept TCP client.
            connTcpServerSockFd, addr = self.__listenTcpServerSockFd.accept()
            if STATUS_ERR == connTcpServerSockFd:
                # No new TCP connection.
                continue
            else:
                # A new TCP connection.
                
                # Create a TCP Server Connection Task.
                task = TcpServerConnTask(connTcpServerSockFd)
                
                # Add a TCP Server Connection Task to the Thread Pool.
                self.__threadPool.addTask(task)
#                 InfoLog(<<"Add a TCP Server Connection Task to the Thread Pool.");
                print("[Info]", "Add a TCP Server Connection Task to the Thread Pool.")
        
        # Close the TCP Server Socket for listening.
        self.__listenTcpServerSockFd.close()
#         InfoLog(<<"Close the TCP Server Socket for listening.");
        print("[Info]", "Close the TCP Server Socket for listening.")
        
        print("[Info]", "TcpServerListenThread - exit")
        
        return STATUS_OK

# end of file
