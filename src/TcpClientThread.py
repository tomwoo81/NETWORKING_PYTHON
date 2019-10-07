#!/usr/bin/env python3
#coding = utf-8

from time import sleep
from socket import *
from threading import Thread
from src.Constants import *
from src.Statuses import *
from src.IpAddr import *

TCP_CLIENT_THREAD_BUFFER_LENGTH = (1 * 1024 * 1024) # 1 MB

'''
class TcpClientThread
'''
class TcpClientThread(Thread):
    def __init__(self, ipVer, strLocalIpAddr, localPortNumber, \
            strRemoteIpAddr, remotePortNumber):
        super().__init__(target = self.run)
        self.__ipVer = ipVer
        self.__strLocalIpAddr = strLocalIpAddr
        self.__localPortNumber = localPortNumber
        self.__strRemoteIpAddr = strRemoteIpAddr
        self.__remotePortNumber = remotePortNumber
    def __del__(self):
        pass

    def run(self):
        print("[Info]", "TcpClientThread - enter")
        
        # Open a TCP Client Socket.
        sockFd = socket(AF_INET if IP_ADDR_VER_4 == self.__ipVer else AF_INET6, \
                                              SOCK_STREAM) # blocking I/O
        if STATUS_ERR == sockFd:
#             ErrLog(<<"Fail to open a TCP Client Socket!");
            print("[Err]", "Fail to open a TCP Client Socket!")
            return STATUS_ERR
        
        # Configure a TCP Client Socket with addr and port.
        ret = sockFd.bind((self.__strLocalIpAddr, self.__localPortNumber))
        if STATUS_ERR == ret:
#             ErrLog(<<"Fail to configure a TCP Client Socket with addr and port!");
            print("[Err]", "Fail to configure a TCP Client Socket with addr and port!")
            return STATUS_ERR
        
        # Connect the TCP server.
        ret = sockFd.connect_ex((self.__strRemoteIpAddr, self.__remotePortNumber))
        if STATUS_OK != ret:
#             ErrLog(<<"Fail to connect the TCP server!");
            print("[Err]", "Fail to connect the TCP server!")
            return STATUS_ERR
        
        for i in range(TCP_CLIENT_TX_MSG_NUM):
            # Send a message.
            txMsg = TCP_CLIENT_TX_MSG % (i, self.__localPortNumber)
            data = txMsg.encode()
            ret = sockFd.send(data)
            if ret != len(data):
#                 WarningLog(<<"Fail to send a message to the TCP server!");
                print("[Warn]", "Fail to send a message to the TCP server!")
                continue
            print("[Info]", "TCP Client (port: {:d}) Tx ({:d}) [{:d} bytes]".format(self.__localPortNumber, i, ret))
            
            data = sockFd.recv(TCP_CLIENT_THREAD_BUFFER_LENGTH)
            if not data:
                # No received message.
                break
            else:
                # A received message.
                
                rxMsg = data.decode()
                print("[Info]", "TCP Client (port: {:d}) Rx ({:d}) [{:d} bytes]".format(self.__localPortNumber, i, len(data)))
                print("[Info]", "TCP Client (port: {:d}) Rx ({:d}): {:s}".format(self.__localPortNumber, i, rxMsg))
            
            sleep(TCP_CLIENT_TX_MSG_INTERVAL)
        
        # Close the TCP Client Socket.
        sockFd.close()
#         InfoLog(<<"Close the TCP Client Socket.");
        print("[Info]", "Close the TCP Client Socket (port: {:d}).".format(self.__localPortNumber))
        
        print("[Info]", "TcpClientThread - exit")
        
        return STATUS_OK

# end of file
