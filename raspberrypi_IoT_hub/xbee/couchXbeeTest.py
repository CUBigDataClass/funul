#! /usr/bin/python

import couchdb
from xbee import ZigBee
import serial
import pprint
import json
from subprocess import check_output

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

couch = couchdb.Server() #default/empty is localhost
db = couch['books']

localIP = check_output(['hostname', '-I'])
localIP = localIP.rstrip()

doc = {'piLocalIP': localIP}
db.save(doc)
print doc

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

# Create API object
xbee1 = ZigBee(ser, escaped=True)

# Continuously read and print packets
while True:
    try:
        response = xbee1.wait_read_frame()
        print(response)
        print "\n"

        #json.dump(response['rf_data'], text_file)

	doc = {'sensor_data': response['rf_data']}
	db.save(doc)
	print doc
        print "\n"

    except KeyboardInterrupt:
        break

ser.close()
