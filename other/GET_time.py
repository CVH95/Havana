#! /usr/bin/env python

# Security in Computer Systems 2018 - SDU.
# HTTP Response Chrono.
# @CarlosViescasHuerta.

import requests
import sys
import time

# Define globals
dst_ip = sys.argv[1]
dst_port = int(sys.argv[2])
_o = '/orders'
_url = 'http://' + dst_ip + ':' + str(dst_port)
_order = _url + _o

# Chrono
ti = time.time()
resp = requests.get(_url)
tf = time.time()
tel = (tf - ti)*1000

# Check
if resp.status_code != 200:
    print ('GET API error ' + str(resp.status_code))
else:
    print("GET request to " + _url)
    print("Response time = " + str(tel) + " ms.")

# Chrono
ti1 = time.time()
resp = requests.get(_order)
tf1 = time.time()
tel1 = (tf1 - ti1)*1000

# Check
if resp.status_code != 200:
    print ('GET API error ' + str(resp.status_code))
else:
    print("GET request to " + _order)
    print("Response time = " + str(tel1) + " ms.")