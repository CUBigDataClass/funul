import serial
import couchdb

COUCHDB_SERVER = 'http://52.14.234.53:5984'

server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.credentials = ('drew', 'admin')
db = server['inventory']

arduinoSerialData=serial.Serial('/dev/ttyACM0',9600)
while 1:
	if(arduinoSerialData.inWaiting()>0):
		myData=arduinoSerialData.readline()
		print myData
