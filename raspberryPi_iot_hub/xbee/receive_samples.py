#! /usr/bin/python

"""
receive_samples.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

This example continuously reads the serial port and processes IO data
received from a remote XBee.
"""

from xbee import ZigBee
import serial
import pprint
import json

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

text_file = open("data.txt", 'w')

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

# Create API object
xbee1 = ZigBee(ser, escaped=True)

# Continuously read and print packets
while True:
    try:
        response = xbee1.wait_read_frame()
        print(response)
        pprint.pprint(response)
        print "\n"

        json.dump(response['rf_data'], text_file)
        text_file.write('\n')

    except KeyboardInterrupt:
        break

text_file.close()      
ser.close()
