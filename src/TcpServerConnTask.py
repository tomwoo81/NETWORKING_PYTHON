#!/usr/bin/env python3
#coding = utf-8

from socket import *
from src.Constants import *
from src.Statuses import *
from src.ThreadPool import PoolTaskIf

TCP_SERVER_TASK_BUFFER_LENGTH = (512 * 1024) # 512 KB

'''
class TcpServerConnTask
'''
class TcpServerConnTask(PoolTaskIf):
    def __init__(self, sockFd):
        self.__sockFd = sockFd
    def __del__(self):
        pass

    def run(self):
        print("[Info]", "TcpServerConnTask - enter")
        
        self.__sockFd.setblocking(True) # blocking I/O
        
        while True:
            data = self.__sockFd.recv(TCP_SERVER_TASK_BUFFER_LENGTH)
            if not data:
                # No received message.
                break
            else:
                # A received message.
                
                rxMsg = data.decode()
                print("[Info]", "TCP Server Rx [{:d} bytes]".format(len(data)))
                print("[Info]", "TCP Server Rx: {:s}".format(rxMsg))
                
                # Send a message.
                txMsg = TCP_SERVER_TX_MSG
                data = txMsg.encode()
                ret = self.__sockFd.send(data)
                if ret != len(data):
#                     WarningLog(<<"Fail to send a message to a TCP client!");
                    print("[Warn]", "Fail to send a message to a TCP client!")
                    continue
                print("[Info]", "TCP Server Tx [{:d} bytes]".format(ret))
        
        # Close the TCP Server Socket for connection.
        self.__sockFd.close()
#         InfoLog(<<"Close the TCP Server Socket for connection.");
        print("[Info]", "Close the TCP Server Socket for connection.")
        
        print("[Info]", "TcpServerConnTask - exit")
        
        return STATUS_OK

# end of file
