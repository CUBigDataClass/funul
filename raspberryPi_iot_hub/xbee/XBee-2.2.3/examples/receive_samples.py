#! /usr/bin/python


"""
receive_samples.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

This example continuously reads the serial port and processes IO data
received from a remote XBee.
"""

from xbee import XBee,ZigBee
import serial
import pprint

PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600


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
	data = response['rf_data']
	
	pprint.pprint(data)
	print "\n"
        text_file = open('data.txt', 'a')
	text_file.write('hrllo')
	text_file.close()
    except KeyboardInterrupt:
        break
        
ser.close()
