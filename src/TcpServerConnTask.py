#!/usr/bin/env python3
#coding = utf-8

from socket import *
from src.Constants import *
from src.Statuses import *
from src.Socket import *
from src.ThreadPool import PoolTaskIf

TCP_SERVER_TASK_BUFFER_LENGTH = (512 * 1024) # 512 KB

'''
class TcpServerConnTask
'''
class TcpServerConnTask(PoolTaskIf):
    def __init__(self, sockFd):
        super().__init__()
        self.__sockFd = sockFd
    def __del__(self):
        if STATUS_ERR != self.__sockFd:
            # Close the TCP Server Socket for connection.
            self.__sockFd.close()
#             InfoLog(<<"Close the TCP Server Socket for connection.");
            print("[Info]", "Close the TCP Server Socket for connection.")
            del self.__sockFd

    def run(self):
        print("[Info]", "TcpServerConnTask - enter")
        
        self.__sockFd.setblocking(False) # Non-blocking I/O
        
        while not self.getThreadPool().isShutdown():
            self.mSleep(10) # Wait for 10 ms.
            
            # Check whether the TCP connection exists.
            status, connected = isConnected(self.__sockFd)
            if (STATUS_OK == status) and (not connected):
#                 InfoLog(<<"A TCP connection is shutdown.");
                print("[Info]", "A TCP connection is shutdown.")
                break
            
            while True:
                try:
                    data = self.__sockFd.recv(TCP_SERVER_TASK_BUFFER_LENGTH)
                except BlockingIOError:
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
#                         WarningLog(<<"Fail to send a message to a TCP client!");
                        print("[Warn]", "Fail to send a message to a TCP client!")
                        continue
                    print("[Info]", "TCP Server Tx [{:d} bytes]".format(ret))
        
        print("[Info]", "TcpServerConnTask - exit")
        
        return STATUS_OK

# end of file
