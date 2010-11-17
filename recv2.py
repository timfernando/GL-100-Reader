#!/usr/bin/env python
# encoding: utf-8
"""
recv.py

Created by Tim Fernando on 2010-11-16.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import socket
import sys
from datetime import datetime
import atexit 

HOST = '' # localhost
PORT = 23456 # change to your preferred listening port

def get_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
	    s.bind((HOST,PORT))
	    return s
    except:
        s.close()
        print "Could not open socket"
        sys.exit(1)

def print_parsed_data(parsed_data):
    print ("-"*35)
    if 'latitude' in parsed_data:
        print "Google Maps Link: http://maps.google.co.uk/?q={0},{1}".format(parsed_data['latitude'],parsed_data['longitude'])

    for key, item in sorted(parsed_data.iteritems()):
        print '{0}: {1}'.format(key,item)
            
def parse_data(data):
    data = data.split(",")
    print "Split Data: "
    print [x for x in data]
    print "-"*35
    
    location_responses = {'GTLBC': "Location Base Call", 'GTTRI': "Timed Report Information",'GTSZI': "Safe Zone Information",'GTSOS': "Save Our Souls",'GTRTL': "Real Time Location"}
    power_responses = {'GTPNA': "Power On Alarm",'GTPFA': "Power Off Alarm",'GTPLA': "Power Low Alarm"}
    unit_information_responses = ['GTCID','GTHWV']
    
    header_type, header_tail = data[0].split(":")
    
    if header_type == '+RESP':
        # Location Responses 
        if header_tail in location_responses:
            print location_responses[header_tail]
            if header_tail == 'GTTRI':
                keys = ['code', 'IMEI', 'responses', 'zone_id', 'zone_alert', 'gps_fix', 'speed', 'heading', 'altitude', 'gps_accuracy', 'longitude', 'latitude', 'send_time']
                return dict(zip(keys,data))
    
            elif header_tail == 'GTLBC':
                keys = ['code', 'IMEI', 'requesting_phone_number', 'uGPS_fix', 'uSpeed', 'heading', 'uAltitude', 'uGPS_accuracy', 'longitude', 'latitude', 'send_time', 'u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7']        
                return dict(zip(keys,data))
    
        # Power Response
        elif header_tail in power_responses:
            print power_responses[header_tail]
            keys = ['code', 'IMEI', 'send_time', 'u1', 'u2']
            return dict(zip(keys,data))
        
        # Hardware/Software Unit Info 
        elif header_tail in unit_information_responses:
            print "CID Information or Hardware Information"
            if header_tail == 'GTCID':
                keys = ['code', 'IMEI', 'CID', 'send_time']
                return dict(zip(keys,data))
            else:
                keys = ['code', 'IMEI', 'hardware_version', 'send_time']
                return dict(zip(keys,data))

        # UNTESTED
        elif header_tail == 'GTHBD':
            print "Heartbeat response from unit"
            keys = ['code', _, 'IMEI', 'send_time']
            return dict(zip(keys,data))
            
        else: return {}

    else:
        print "Received Acknowledgement Message"
        return {}
        
def main():
    s = get_socket()
    while 1:
        s.listen(1)
        print "Listening on port", PORT, "..."
        conn,addr = s.accept()
        print 'Connected by', addr, "at ", datetime.now()
        while 1:
            data = conn.recv(2056)
            if not data: break
            print("="*50)
            print "Unparsed: ", data
            print ("-"*35)
            parsed_data = parse_data(data)
            print_parsed_data(parsed_data)
            print("="*50)
            
            with open('default.output', 'a') as f:
                f.write(data)
                f.write('\n')
    s.close()
    f.close()


if __name__ == '__main__':
    main()

