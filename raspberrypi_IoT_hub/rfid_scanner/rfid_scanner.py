import serial
import couchdb

COUCHDB_SERVER = 'http://52.15.234.53:5984'

server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.credentials = ('admin','drewmeyers#1')
db = server['inventory']


#arduinoSerialData=serial.Serial('/dev/ttyUSB0',115200)


query_fun = """functin(doc) {
	if (doc.type == 'item')  {
        	emit(doc.name, null);

	}
}
"""


while 1:
#	print("in loop")	
#	if(arduinoSerialData.inWaiting()>0):
 #    		myData=arduinoSerialData.readline()


#		for row in db:
#			print(row)
	        for row in db.temporary_query(query_fun):
	       		print("query is: ",row)
#        	print("the Epc is: ", myData)
