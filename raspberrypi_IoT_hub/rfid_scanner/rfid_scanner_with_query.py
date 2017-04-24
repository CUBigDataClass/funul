import json
import couchdb
import serial
import time
import funul_email

COUCHDB_SERVER = 'http://52.14.61.109:5984'

server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.creidentials = ('admin','drewmeyes#1')
db = server['items']

arduinoSerialData=serial.Serial('/dev/ttyUSB0',115200)

last_change = 0
items = []

total = 0.0
last_time_check = time.time()

def fun(doc,data,items_arr):
	#print(doc['gid'])
	if data == doc['gid']:
		#total += doc['price']
		#print("found")
		items_arr.append(doc['item_Name'])
		return(doc['price'])
	else:
		return(0)

while 1:
#	if (int(time.time() - last_time_check) > last_change):	
#		print(int(time.time() - last_time_check))
#		last_change = int(time.time() - last_time_check)
	if (arduinoSerialData.inWaiting()>0):
		myData = arduinoSerialData.readline()
		myData.replace(" ","")
		open_bracket_index = myData.find("[") + 1
		closed_bracket_index = myData.find("]") - 1
		myData = myData[open_bracket_index:closed_bracket_index]
#		print("before for")
	#	print("data from dev ",myData)
		for row in db:
			price =  fun(db.get(row),myData,items)
			if (price != 0):
				last_change = 0
				last_time_check = time.time()		
			total = total + price
		#print(myData)
			if (price != 0):
				print(chr(27) + "[2J")
				print(total)
				print(items)
		if (total == 0):
			print(myData)
	if (time.time() - last_time_check > 30):
		funul_email.sendMail(items,total)
		last_time_check = 9999999999999999999
		items = []
		total = 0
		#print(myData)


#print(h)
#list(db.temporary_query(map_func))
