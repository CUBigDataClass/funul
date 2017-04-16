import serial

output = ""
ser = serial.Serial('/dev/ttyUSB0', 9600, 8, 'N', 1, timeout=1)

while True:
	print "--------"
	while output != "suh":
		output = ser.readline()
		print output

