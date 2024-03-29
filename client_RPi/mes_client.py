#!/usr/bin/python

import mes_api
import sys
import socket


# Robot System Design 2018 - SDU
# REST API Client of the project's MES System
# @CarlosViescasHuerta.

print ("##################################")
print ("##  WORKCELL #3 ONLINE MANAGER  ##")
print ("################################## \n")

_arg = sys.argv[1]
_arg2 = sys.argv[2]
_ip_addrr = str(_arg)
_plc_addrr = str(_arg2)
print ("MES server's IP address: " + _ip_addrr)
print ("PLC server's IP address: " + _plc_addrr)

# Define url and paths
_url = 'http://' + _ip_addrr + ':5000'
_log = '/log'
_orders = '/orders'
_events = '/event_types'
_ticket = '/ticket'
#_host = 'localhost'

# Define global variables
cell_id = 3
events_dict = {0:'PML_Idle', 1:'PML_Execute', 2:'PML_Complete', 3:'PML_Held', 4:'PML_Suspended', 5:'PML_Aborted', 6:'PML_Stopped', 7:'Order_Start', 8:'Order_Done'}

#mysql = MySQL()

# Create a TCP/IP socket client connected to PLC's server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (_plc_addrr, 3000)
sock.connect(server_address)

print ("Connected to PLC's Server in http://" + server_address[0] + ":3000/")

while True:

    print ("Connecting to server on " + _url + " and waiting for new jobs \n")
    
    ##################################################################
    # 1. SEE ORDERS -- Call GET method to see list of available jobs #
    ##################################################################
    
    resp = mes_api.get_orders(_url, _orders)
    if resp.status_code != 200:
        print ("Raised API Error on GET request. Status code " + str(resp.status_code))
    else:
        print ("GET request " + _url + _orders + " succesful")
        mes_api.get_time(resp.status_code) 

        # Create JSON object
        jsonObj = resp.json()
    
        # Check & Print JSON object array length
        lgth = len(jsonObj['orders'])
        #print "  >> JSON object length = " + str(lgth) + "\n"

        # Seek for orders with status == ready
        for i in range(0, lgth):
            if jsonObj['orders'][i]['status'] == 'ready':
                _id = jsonObj['orders'][i]['id']
                # Array that will be sent to the PLC
                _plc = [jsonObj['orders'][i]['blue'], jsonObj['orders'][i]['red'], jsonObj['orders'][i]['yellow'], _id]
                print ("Taking order #" + str(_id))
                print ("Updated order with id: " + str(_id))
                print ("Preparing LEGO bricks:")
                print ("  >> Blue: " + str(jsonObj['orders'][i]['blue']))
                print ("  >> Red: " + str(jsonObj['orders'][i]['red']))
                print ("  >> Yellow: " + str(jsonObj['orders'][i]['yellow']))
                print ("\n")
                break
            else:
                _id = -1

        
    # Handling situation in which no order is avaliable.
    if _id == -1:
        cerr = "waiting - all orders taken"
        rerr = mes_api.post_log(_url, _log, cell_id, cerr, events_dict[0])
        if rerr.status_code != 200:
            print ("Raised API Error on POST request. Status code " + str(rerr.status_code) + "\n")
        else:
            print ("POST request indicating No-Order status to" + _url + " succesful")
            mes_api.get_time(rerr.status_code)
            mes_api.die(8)

    else:
        #####################################################
        # 2. TAKE ORDER -- Call PUT method to take an order #
        #####################################################

        r = mes_api.put_order(_url, _orders, _id)
        if r.status_code != 200:
            print ("Raised API Error on PUT request. Status code " + str(r.status_code))
        else:
            print ("PUT request " + _url + _orders + " succesful")
            mes_api.get_time(r.status_code)

            # GET ticket request
            r77 = mes_api.get_ticket(_id, _url, _ticket, _orders)
            if r77.status_code != 200:
                print ("Raised API Error on PUT request. Status code " + str(r77.status_code))
                ticket = "unknown"
            else:
                print ("GET request " + _url + _orders + "/" + str(_id) + _ticket + " succesful")
                mes_api.get_time(r77.status_code)
                jsonTKT = r77.json()
                ticket = jsonTKT['order'][0]['ticket']
                print ("Order " + str(_id) + " ticket: " + str(ticket) + "\n")

            # Call GET method to see 
            r2 = mes_api.get_single(_url, _orders, _id)
            if r2.status_code != 200:
                print ("Raised API Error on GET. Status code " + str(r2.status_code))
            else:
                print ("GET request " + _url + _orders + " succesful")
                mes_api.get_time(r2.status_code)

                # Call POST method to add new log entry on Order_Start
                _idstr = str(_id)
                cmnt = _idstr + ": " + str(ticket)
                r3 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[7])
                if r3.status_code != 200:
                    print ("Raised API Error on POST request. Status code " + str(r3.status_code))
                else:
                    print ("POST request " + _url + _orders + " succesful")
                    mes_api.get_time(r3.status_code)


            #####     Order processing      #####
            print ("Processing order...")
            #mes_api.die(15)
            mes_api.plc_control(sock, _plc, events_dict, _url, _log, cell_id, cmnt)


            ##### PackML related code here  #####

            
            ##########################################################################
            # 3. DELETE ORDER -- Call DELETE method to erase completed order from DB #
            ##########################################################################
            resp = mes_api.delete_order(_url, _orders, _id)
            if resp.status_code != 200:
                print ("Raised API Error on DELETE request. Status code " + str(resp.status_code))
            else:
                print ("DELETE request " + _url + _orders + " succesful")
                mes_api.get_time(resp.status_code) 

                # Log entry indicating deletion of the complete order
                r4 = mes_api.post_log(_url, _log, cell_id, cmnt, events_dict[8])
                if r4.status_code != 200:
                    print ("Raised API Error on POST request. Status code " + str(r4.status_code))
                else:
                    print ("POST request " + _url + _orders + " succesful")
                    mes_api.get_time(r4.status_code)
                    print ("\n")

            mes_api.die(5)        


# Never ending loop