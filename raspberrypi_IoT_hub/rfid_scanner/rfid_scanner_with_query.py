import json
import couchdb
import serial

COUCHDB_SERVER = 'http://52.14.61.109:5984'

server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.creidentials = ('admin','drewmeyes#1')
db = server['items']

arduinoSerialData=serial.Serial('/dev/ttyUSB0',115200)

def fun(doc):
	if "0000000" == doc['uid']:
		print("found")
		return(doc)

while 1:
	if(arduinoSerialData.inWaiting()>0):
		myData = arduinoSerialData.readline()
		open_bracket = myData.find("[")
		closed_bracket = myData.find("]")

		for row in db:
			fun(db.get(row))
		print(myData)

#print(h)
#list(db.temporary_query(map_func))
