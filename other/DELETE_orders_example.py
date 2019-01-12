#!/usr/bin/python

# Flush jobs table

import requests

_url = 'http://192.168.1.100:5000'
_orders = '/orders'
g_url = _url + _orders

resp = requests.get(g_url)
# Create JSON object
jsonObj = resp.json()
    
# Check & Print JSON object array length
lgth = len(jsonObj['orders'])
for i in range(0, lgth-1):
    _id = jsonObj['orders'][i]['id']
    _idstr = str(_id)
    _idd = '/' + _idstr
    d_url = g_url + _idd
    r = requests.delete(d_url)

print "Flushed some jobs in the database"
