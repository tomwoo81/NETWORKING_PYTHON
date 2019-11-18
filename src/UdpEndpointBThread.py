#!/usr/bin/env python3
#coding = utf-8

from time import sleep
from socket import *
from threading import Thread
from src.Constants import *
from src.Statuses import *
from src.IpAddr import *

UDP_ENDPOINT_B_THREAD_BUFFER_LENGTH = (1 * 1024 * 1024) # 1 MB

'''
class UdpEndpointBThread
'''
class UdpEndpointBThread(Thread):
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
        print("[Info]", "UdpEndpointBThread - enter")
        
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
        
        for i in range(UDP_ENDPOINT_B_TX_MSG_NUM):
            # Send a message.
            txMsg = UDP_ENDPOINT_B_TX_MSG % (i, self.__localPortNumber)
            data = txMsg.encode()
            ret = sockFd.sendto(data, (self.__strRemoteIpAddr, self.__remotePortNumber))
            if ret != len(data):
#                 WarningLog(<<"Fail to send a message to the UDP Peer Endpoint!");
                print("[Warn]", "Fail to send a message to the UDP Peer Endpoint!")
                continue
            print("[Info]", "UDP Endpoint (port: {:d}) Tx ({:d}) [{:d} bytes]".format(self.__localPortNumber, i, ret))
            
            data, addr = sockFd.recvfrom(UDP_ENDPOINT_B_THREAD_BUFFER_LENGTH)
            if not data:
                # No received message.
                break
            else:
                # A received message.
                
                rxMsg = data.decode()
                print("[Info]", "UDP Endpoint (port: {:d}) Rx ({:d}) [{:d} bytes]".format(self.__localPortNumber, i, len(data)))
                print("[Info]", "UDP Endpoint (port: {:d}) Rx ({:d}): {:s}".format(self.__localPortNumber, i, rxMsg))
            
            sleep(UDP_ENDPOINT_B_TX_MSG_INTERVAL)
        
        # Close the UDP Endpoint Socket.
        sockFd.close()
#         InfoLog(<<"Close the UDP Endpoint Socket.");
        print("[Info]", "Close the UDP Endpoint Socket (port: {:d}).".format(self.__localPortNumber))
        
        print("[Info]", "UdpEndpointBThread - exit")
        
        return STATUS_OK

# end of file
