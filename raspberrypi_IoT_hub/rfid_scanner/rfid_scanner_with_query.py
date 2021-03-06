import json
import couchdb
import serial
import time
import funul_email

from texttable import Texttable
from tabulate import tabulate

COUCHDB_SERVER = 'http://52.14.61.109:5984'

server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.creidentials = ('admin','drewmeyes#1')
db = server['items']

arduinoSerialData=serial.Serial('/dev/ttyUSB0',115200)

last_change = 0
items = []
table = [['Items','Price']]
total = 0.0
last_time_check = time.time()


def fun(doc,data,items_arr,print_table):
	#print(doc['gid'])
	if data == doc['gid']:
		#total += doc['price']
		#print("found")
		print_table.append([doc['item_Name'],doc['price']])
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
			price =  fun(db.get(row),myData,items,table)
			if (price != 0):
				last_change = 0
				last_time_check = time.time()		
			total = total + price
		#print(myData)
			if (price != 0):
				print(chr(27) + "[2J")
				t = Texttable()
				t.add_rows(table)
				cur_table = t.draw()
				print(cur_table)
				#print('\n'.join(items))
				print("Total cost: " + str(total))
		if (total == 0):
			print(myData)
	if (time.time() - last_time_check > 10 and len(items)!=0):
		print(chr(27)+"[2J")
		print("Thank you for shopping with us")
		table = [['Items','Price']]
		cur_table.replace(","," ")
		#send_table = tablulate(table)
		funul_email.sendMail(items,total)
		last_time_check = 9999999999999999999
		items = []
		total = 0
		time.sleep(3)
		print(chr(27)+"[2J")
		print("Hello, Please Scan Items")
		#print(myData)


#print(h)
#list(db.temporary_query(map_func))
