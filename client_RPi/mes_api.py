#!/usr/bin/python

import requests
import time
import pymysql.cursors
import pymysql
import socket
import sys

# Robot System Design 2018 - SDU
# API of the project's MES System
# Carlos, Caroline, Daniel

# Print current timestamp
def get_time(stcode):
    print ("On " + time.strftime("%c") + " - Status code = " + str(stcode) + "\n")

# Get order list (GET)
def get_orders(_url, path):
    g_url = _url + path
    return requests.get(g_url)

# Get single order (GET)
def get_single(_url, path, s):
    _ids = '/' + str(s)
    gs_url = _url + path + _ids
    return requests.get(gs_url)

# Take order (PUT)
def put_order(_url, path, x):
    _idx = '/' + str(x)
    pt_url = _url + path + _idx
    return requests.put(pt_url) 

# Sleeping 
def die(secs):
    time.sleep(secs)

def get_ticket(_id, _url, _ticket, _orders):
    _ids = '/' + str(_id)
    t_url = _url + _orders + _ids + _ticket
    return requests.get(t_url)


############################################################################################
# OLD FUNCTION Get ticket from database
#def get_ticket(_id, hoost):
#    # Connect to database
#    conn = pymysql.connect(host=hoost,
#                           user='scs',
#                           password='scs2018',
#                           db='scs2018',
#                           charset='utf8',
#                           cursorclass=pymysql.cursors.DictCursor)
#    
#    try:
#        with conn.cursor() as cursor:
            # Select ticket 
#            select_stmt = "select id, ticket from scs2018.jobs where id = %s"
#            cursor.execute(select_stmt, _id)
#            result = cursor.fetchone()
#    finally:
            # Close connection
#        conn.close()
    
#    return result
############################################################################################

# Log system state (POST)
def post_log(_url, path, cid, cmnt, evt):
    log = {"cell_id": cid, "comment": cmnt, "event": evt}
    print ("Posted new log entry:")
    print ("  >> cell_id: " + str(cid))
    print ("  >> event: " + evt)
    print ("  >> cmnt: " + cmnt)
    pst_url = _url + path
    return requests.post(pst_url, json=log)

# Delete an order (DELETE)
def delete_order(_url, path, d):
    _idd = '/' + str(d)
    d_url = _url + path + _idd
    return requests.delete(d_url)

# PLC communication during the processing of the order
def plc_control(sock, _plc, events, _url, _path, cid, cmt):

    # Send hello message
    hello = 'hi'
    hello_msg = hello.encode()
    sock.send(hello_msg)
    print ("Sent hello message.")

    while True:
        ti = time.time()
        rec = sock.recv(1024)
        tf = time.time()
        tel = (tf-ti)*1000
        if str(rec.decode()) == 'new':
            print ("Received 'new' request. Preparing order to be sent.")
            print ("Response time = " + str(tel) + " ms.")
            break
        else:
            print ("Received the following message: " + str(rec.decode()))

     
    data_raw = '(' + str(_plc[0]) + ',' + str(_plc[1]) + ',' + str(_plc[2]) + ')'
    data = data_raw.encode()

    sock.send(data)
    print ("Sent order to PLC: " + data_raw)

    while True:
        ti1 = time.time()
        rs = sock.recv(1024)
        tf1 = time.time()
        tel1 = (tf1-ti1)*1000
        if rs != None:
            rst = rs.decode()
            print ("Server's reply: " + str(rst))
            if str(rst) == 'ok':
                print ("Server received the order, now waiting for updates...")
                print ("Response time = " + str(tel1) + " ms.")
                while True:
                    ti2 = time.time()
                    rcpt = sock.recv(1024)
                    tf2 = time.time()
                    tel2 = (tf2-ti2)*1000
                    _state = int(rcpt)
                    if _state == 2:
                        print ("Server's reply:")
                        print ("PackML state update: " + events[_state])
                        print ("Response time = " + str(tel2) + " ms.")
                        break
                    else:
                        print ("Server's reply:")
                        print ("PackML state update: " + events[_state])
                        print ("Response time = " + str(tel2) + " ms.")
                        evt = events[_state]
                        post_log(_url, _path, cid, cmt, evt)
                    break
            
            else:
                print ("Server's reply: " + str(rst))
                print ("An error ocurred while processing the order")
                print ("Response time = " + str(tel1) + " ms.")
                break
        
        else:
            print("Did not receive anything from PLC")

#sock.close()
#print ("Connection closed.")