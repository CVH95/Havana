#!/usr/bin/python

import socket
import sys
import random
import time

_ip = str(sys.argv[1])
#_ip = 'localhost'
_port = 3000

# Int checking for validating the orders received.
def isint(a):
    try:
        int(a)
        return True
    except ValueError:
        return False

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
    hhh = _order.decode()
    order = str(hhh)
    l1 = len(order)

    # Check if it is a hello message.
    if order == 'hi':
        print ("Received hello message: " + order)
        msn = 'new'
        m = msn.encode()
        c.send(m)
        print ("Sent: " + msn)

    # Check the length or the order and the data type.
    elif l1 == 7 and order[0] == '(' and isint(order[1]) and order[2] == ',' and isint(order[3]) and order[4] == ',' and isint(order[5]) and order[6] == ')':
    
        # Check that the number of bricks per color is within package limits:
        if int(order[1]) <= 4 and int(order[3]) <= 4 and int(order[5]) <= 2:
        
            # 2. Robot starts working. PackML sends (random) state updates to MES system via socket.

            print("Order: " + order + "  |  Length = " + str(l1))
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
                time.sleep(1.5)
                i = i + 1
            eoc = 2
            i = 0
            _eoc = str(eoc)
            e = _eoc.encode()
            c.send(e)
            print ("Back to start \n \n")

        else:
                
            print("Received an invalid order: " + order + "  |  Length = " + str(l1))

    else:
        print("Received unknown message:")
        print("Message: " + order + "  |  Length = " + str(l1))