#!/usr/bin/env python3
#coding = utf-8

from socket import *
from src.Statuses import *

TCP_ESTABLISHED = 1

def isConnected(sockFd):
    # Get the TCP info of the socket.
    bTcpInfo = sockFd.getsockopt(IPPROTO_TCP, TCP_INFO, 256)
    if not bTcpInfo:
        print("[Warn]", "Fail to get the TCP info of the socket!")
        return (STATUS_ERR, False)
    
    tcpState = bTcpInfo[0]
    if TCP_ESTABLISHED == tcpState:
        connected = True
#         print("TCP state: established")
    else:
        connected = False
#         print("TCP state: {:d}".format(tcpState))
    
    return (STATUS_OK, connected)

if __name__ == "__main__":
    status, connected = isConnected()
    print("[Info]", "Status: {:d}, Connected: {:d}".format(status, connected))

# end of file
