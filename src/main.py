#!/usr/bin/env python3
#coding = utf-8

from os import fork, wait
from sys import argv, exit
from time import sleep
from src.Constants import *
from src.Statuses import *
from src.IpAddr import *
from src.TcpServerListenThread import TcpServerListenThread
from src.TcpClientThread import TcpClientThread
from src.UdpEndpointAThread import UdpEndpointAThread
from src.UdpEndpointBThread import UdpEndpointBThread

def tcpMain():
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

def udpMain():
    print("[Info]", "Main process - enter")
    
    pid = fork()
    if pid < 0:
        # Main process
        print("[Err]", "Fail to fork a child process!")
        print("[Info]", "Main process - exit")
        exit(STATUS_ERR)
    elif 0 == pid:
        # Child process for UDP endpoint A
        print("[Info]", "Child process for UDP endpoint A - enter")
        
        udpEndpointAThread = UdpEndpointAThread\
                (IP_ADDR_VER_4, UDP_ENDPOINT_A_IP_ADDR, UDP_ENDPOINT_A_PORT_NUMBER)
        
        udpEndpointAThread.start()
        
        sleep(UDP_ENDPOINT_A_RUNNING_DURATION)
        
        udpEndpointAThread.shutdown()
        udpEndpointAThread.join()
        del udpEndpointAThread
        
        print("[Info]", "Child process for UDP endpoint A - exit")
        exit(STATUS_OK)
    else:
        # Main process
        for i in range(NUM_UDP_ENDPOINTS_B):
            sleep(UDP_ENDPOINT_B_TX_MSG_INTERVAL)
            
            pid = fork()
            if pid < 0:
                # Main process
                print("[Err]", "Fail to fork a child process!")
                print("[Info]", "Main process - exit")
                exit(STATUS_ERR)
            elif 0 == pid:
                # Child process for UDP endpoint B
                print("[Info]", "Child process for UDP endpoint B {:d} - enter".format(i))
                
                udpEndpointBThread = UdpEndpointBThread\
                (IP_ADDR_VER_4, UDP_ENDPOINT_B_IP_ADDR, UDP_ENDPOINT_B_PORT_NUMBER_BASE + i,\
                                UDP_ENDPOINT_A_IP_ADDR, UDP_ENDPOINT_A_PORT_NUMBER)
                
                udpEndpointBThread.start()
                
                udpEndpointBThread.join()
                del udpEndpointBThread
                
                print("[Info]", "Child process for UDP endpoint B {:d} - exit".format(i))
                exit(STATUS_OK)
        
        # Wait for shutdown of all child processes.
        while True:
            try:
                wait()
            except ChildProcessError:
                break
        
        print("[Info]", "Main process - exit")
        exit(STATUS_OK)

def main(argv):
    argc = len(argv)
    
    if argc >= 2:
        socketType = argv[1]
    
    if "tcp" == socketType.lower():
        return tcpMain()
    elif "udp" == socketType.lower():
        return udpMain()
    else:
        print("[Info]", "The type ({}) is invalid!".format(socketType))
        return STATUS_ERR
    
    return STATUS_OK

if __name__ == "__main__":
    main(argv)

# end of file
