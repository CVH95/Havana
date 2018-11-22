#!/usr/bin/python

# REAL PLC:
    # Select library tcpIp
    # Download TCP/IP License: Licenses - Manage licenses - tcpIp - 7 days
    # Import modules of the library into the program
    # Connect to PLC remote desktop and install package tf6310 tcpIp or something like that is called

import socket
import sys
import random
import time

_ip = 'localhost'
_port = 30000

print "PLC running TCP/IP Server on http://" + _ip + ":" + str(_port) + "/"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((_ip, _port))
server.listen(5)  # max backlog of connections
(c, addr) = server.accept() 



while (True): 
    print "Accepted connection from {}:{}".format(addr[0], addr[1])

    # 1. Receive list of lego bricks = array[4]
        # index =
            # 0: blue
            # 1: red
            # 2: yellow
            # 3: order id
    _order = c.recv(1024)

    if _order != '':
        
        # 2. Robot starts working. PackML sends state updates to MES system via socket.

        print "Order: " + _order
        i = 0
        j = random.randint(2,6)
        while (i<j):
            a = random.randint(0,6)
            _a = str(a)
            c.send(_a)
            print "Sending PackML state upadate."
            i = i + 1
            time.sleep(3)
        eoc = 9
        i = 0
        _eoc = str(eoc)
        c.send(_eoc)
        break

print "Server shut down"