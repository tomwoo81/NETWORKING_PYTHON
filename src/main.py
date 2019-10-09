#!/usr/bin/env python3
#coding = utf-8

from os import fork, wait
from sys import exit
from time import sleep
from src.Constants import *
from src.Statuses import *
from src.IpAddr import *
from src.TcpServerListenThread import TcpServerListenThread
from src.TcpClientThread import TcpClientThread

print("[Info]", "Main process - enter")

pid = fork()
if pid < 0:
    # Main process
    print("[Err]", "Fail to fork a child process!")
    print("[Info]", "Main process - exit")
    exit(STATUS_ERR)
elif 0 == pid:
    # Child process for TCP server
    print("[Info]", "Child process for TCP server - enter")
    
    tcpServerListenThread = TcpServerListenThread\
            (IP_ADDR_VER_4, TCP_SERVER_IP_ADDR, TCP_SERVER_PORT_NUMBER)
    
    tcpServerListenThread.start()
    
    sleep(TCP_SERVER_RUNNING_DURATION)
    
    tcpServerListenThread.shutdown()
    tcpServerListenThread.join()
    del tcpServerListenThread
    
    print("[Info]", "Child process for TCP server - exit")
    exit(STATUS_OK)
else:
    # Main process
    for i in range(NUM_TCP_CLIENTS):
        sleep(TCP_CLIENT_TX_MSG_INTERVAL)
        
        pid = fork()
        if pid < 0:
            # Main process
            print("[Err]", "Fail to fork a child process!")
            print("[Info]", "Main process - exit")
            exit(STATUS_ERR)
        elif 0 == pid:
            # Child process for TCP client
            print("[Info]", "Child process for TCP client {:d} - enter".format(i))
            
            tcpClientThread = TcpClientThread(IP_ADDR_VER_4, TCP_CLIENT_IP_ADDR, TCP_CLIENT_PORT_NUMBER_BASE + i,\
                                              TCP_SERVER_IP_ADDR, TCP_SERVER_PORT_NUMBER)
            
            tcpClientThread.start()
            
            tcpClientThread.join()
            del tcpClientThread
            
            print("[Info]", "Child process for TCP client {:d} - exit".format(i))
            exit(STATUS_OK)
    
    # Wait for shutdown of all child processes.
    while True:
        try:
            wait()
        except ChildProcessError:
            break
    
    print("[Info]", "Main process - exit")
    exit(STATUS_OK)

# end of file
