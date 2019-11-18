#!/usr/bin/env python3
#coding = utf-8

from socket import *
from threading import Thread, Lock, Condition
from src.Constants import *
from src.Statuses import *
from src.IpAddr import *

UDP_ENDPOINT_A_THREAD_BUFFER_LENGTH = (1 * 1024 * 1024) # 1 MB

'''
class UdpEndpointAThread
'''
class UdpEndpointAThread(Thread):
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
        print("[Info]", "UdpEndpointAThread - enter")
        
        # Open a UDP Endpoint Socket.
        sockFd = socket(AF_INET if IP_ADDR_VER_4 == self.__ipVer else AF_INET6, \
                                              SOCK_DGRAM) # blocking I/O
        if STATUS_ERR == sockFd:
#             ErrLog(<<"Fail to open a UDP Endpoint Socket!");
            print("[Err]", "Fail to open a UDP Endpoint Socket!")
            return STATUS_ERR
        
        # Configure a UDP Endpoint Socket with addr and port.
        ret = sockFd.bind((self.__strLocalIpAddr, self.__localPortNumber))
        if STATUS_ERR == ret:
#             ErrLog(<<"Fail to configure a UDP Endpoint Socket with addr and port!");
            print("[Err]", "Fail to configure a UDP Endpoint Socket with addr and port!")
            return STATUS_ERR
        
        sockFd.setblocking(False) # Non-blocking I/O
        
        while not self.__waitForShutdown(10): # Wait for 10 ms.
            while True:
                try:
                    data, addr = sockFd.recvfrom(UDP_ENDPOINT_A_THREAD_BUFFER_LENGTH)
                except BlockingIOError:
                    # No received message.
                    break
                else:
                    # A received message.
                    
                    rxMsg = data.decode()
                    print("[Info]", "UDP Endpoint Rx [{:d} bytes]".format(len(data)))
                    print("[Info]", "UDP Endpoint Rx: {:s}".format(rxMsg))
                    
                    # Send a message.
                    txMsg = UDP_ENDPOINT_A_TX_MSG
                    data = txMsg.encode()
                    ret = sockFd.sendto(data, addr)
                    if ret != len(data):
#                         WarningLog(<<"Fail to send a message to a UDP Peer Endpoint!");
                        print("[Warn]", "Fail to send a message to a UDP Peer Endpoint!")
                        continue
                    print("[Info]", "UDP Endpoint Tx [{:d} bytes]".format(ret))
        
        # Close the UDP Endpoint Socket.
        sockFd.close()
#         InfoLog(<<"Close the UDP Endpoint Socket.");
        print("[Info]", "Close the UDP Endpoint Socket (port: {:d}).".format(self.__localPortNumber))
        
        print("[Info]", "UdpEndpointAThread - exit")
        
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
