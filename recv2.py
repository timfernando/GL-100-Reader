#!/usr/bin/env python
# encoding: utf-8
"""
recv2.py

Created by Tim Fernando on 2010-11-16.
Copyright (c) 2010 University of Oxford. All rights reserved.
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
    power_responses = {'GTPNA': "Power On Alarm",'GTPFA': "Power Off Alarm",'GTPLA': "Power Low Alarm", 'GTCBC': "Battery Check Response"}
    general_information_responses = {'GTCID': "CID Info?",'GTHWV': "Hardware Information?", 'GTINF': "General Information?"}
    
    header_type, header_tail = data[0].split(":")
    
    if header_type == '+RESP':
        # Location Responses 
        if header_tail in location_responses:
            print location_responses[header_tail]
            if header_tail == 'GTTRI': # Possible to have variable entries here
                keys = ['code', 'IMEI', 'responses', 'zone_id', 'zone_alert', 'gps_fix', 'speed', 'heading', 'altitude', 'gps_accuracy', 'longitude', 'latitude', 'send_time', 'u234', 'u10', 'u08d2']
            elif header_tail == 'GTRTL': # GTRTL does not use the 'responses' field
                keys = ['code', 'IMEI', 'UNUSED' , 'zone_id', 'zone_alert', 'gps_fix', 'speed', 'heading', 'altitude', 'gps_accuracy', 'longitude', 'latitude', 'send_time', 'u234', 'u10', 'u08d2', 'u1', 'u2', 'message_id', 'u99']
            elif header_tail == 'GTLBC':
                keys = ['code', 'IMEI', 'requesting_phone_number', 'gps_fix', 'speed', 'heading', 'uAltitude', 'uGPS_accuracy', 'longitude', 'latitude', 'send_time', 'u234', 'u10', 'u08d2', 'u1', 'u2', 'message_id', 'u99']        
            else:  # GTSZI, GTSOS -- Probably similar to GTTRI/GTRTL
                keys = ['code', 'IMEI']
            return dict(zip(keys,data))
    
        # Power Response
        # TESTED
        elif header_tail in power_responses:
            print power_responses[header_tail]
            if header_tail == 'GTCBC': 
                keys = ['code', 'IMEI', 'battery_charge', 'send_time', 'message_id', 'u99']
            else: # GTPNA, GTPLA, GTPFA
                keys = ['code', 'IMEI', 'send_time', 'message_id', 'u99']
            return dict(zip(keys,data))    
        
        # Hardware/Software/Sim Info 
        # TWO UNTESTED
        elif header_tail in general_information_responses:
            print general_information_responses[header_tail]
            if header_tail == 'GTINF': # Checked
                keys = ['code', 'IMEI', 'sim_id', 'uINF_1', 'uINF_2', 'battery_charge', 'uINF_3', 'send_time', 'message_id', 'u99']
            elif header_tail == 'GTCID': # TODO Untested
                keys = ['code', 'IMEI', 'CID', 'send_time']
            else: # GTHWV -- TODO Untested
                keys = ['code', 'IMEI', 'hardware_version', 'send_time']
            return dict(zip(keys,data))

        # Heartbeat Response - only happens when a persistent GPRS session is active
        # UNTESTED
        elif header_tail == 'GTHBD':
            print "Heartbeat response from unit"
            keys = ['code', _, 'IMEI', 'send_time']
            return dict(zip(keys,data))
            
        # GTGEO - Unknown
        # UNTESTED
        elif header_tail == 'GTGEO':
            print "GTGEO Response"
            return {}
    
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

