#!/usr/bin/env python3
#coding = utf-8

TCP_SERVER_IP_ADDR = "127.0.0.1" #Loopback Address
TCP_SERVER_PORT_NUMBER = 8888
TCP_CONNECTIONS_MAX_NUM = 5
THREAD_POOL_NUM_THREADS = 3
TCP_SERVER_TX_MSG = "Response from TCP Server to TCP Client"
TCP_SERVER_RUNNING_DURATION = 40 #Unit: second

TCP_CLIENT_IP_ADDR = "127.0.0.1" #Loopback Address
TCP_CLIENT_PORT_NUMBER_BASE = 33500
TCP_CLIENT_TX_MSG_NUM = 5
TCP_CLIENT_TX_MSG_INTERVAL = 3 #Unit: second
TCP_CLIENT_TX_MSG = "Request (%u) from TCP Client (port: %u) to TCP Server"
NUM_TCP_CLIENTS = 5

#SOFTWARE_VERSION = "V10.01.00.00"

# end of file
