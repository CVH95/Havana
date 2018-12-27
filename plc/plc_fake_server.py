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

#_ip = str(sys.argv[1])
_ip = 'localhost'
_port = 30000

print ("PLC running TCP/IP Server on http://" + _ip + ":" + str(_port) + "/")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((_ip, _port))
server.listen(5)  # max backlog of connections
(c, addr) = server.accept() 

while (True): 

    print ("Accepted connection from {}:{}".format(addr[0], addr[1]))

    # 1. Receive list of lego bricks = array[4]
        # index =
            # 0: blue
            # 1: red
            # 2: yellow
            # 3: order id
    
    _order = c.recv(1024)
    order = _order.decode()

    if str(order) == 'hi':
        print ("Received hello message: " + str(_order))
        msn = 'new'
        m = msn.encode()
        c.send(m)
        print ("Sent: " + msn)

    else:
        
        # 2. Robot starts working. PackML sends state updates to MES system via socket (Here, random states are sent).

        print ("Order: " + str(order))
        msn = 'ok'
        z = msn.encode()
        c.send(z)
        print ("Sent ok")
        i = 0
        j = random.randint(2,6)
        print ("Number of rounds = " + str(j))
        while (i<j):
            a = random.randint(0,6)
            if a == 2:
                a = 3
            else:
                a = a
            _a = str(a)
            aa = _a.encode()
            c.send(aa)
            print ("Sending PackML state upadate.")
            time.sleep(3)
            i = i + 1
        eoc = 2
        i = 0
        _eoc = str(eoc)
        e = _eoc.encode()
        c.send(e)
        print ("Back to start \n \n")