# test BLE Scanning software
# jcs 6/8/2014

import couchdb
import blescan
import sys
import bluetooth._bluetooth as bluez
from subprocess import check_output
import time

pi_id = "pi_4"

couch = couchdb.Server() #default/empty is localhost
db = couch['local_ip']

localIP = check_output(['hostname', '-I'])
localIP = localIP.rstrip()

epoch_time = time.time()
doc = {'piLocalIP': localIP, 'pi_id': pi_id, 'piLocalIP': localIP, 'epoch_time': epoch_time}
db.save(doc)
print doc

db = couch['ble']
dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print ("ble thread started")

except:
	print ("error accessing bluetooth device...")
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
	returnedList = blescan.parse_events(sock, 10)
	print ("----------")
	for beacon in returnedList:
		mac = beacon.split(",")[0]
		if mac == "0c:f3:ee:00:eb:ea": #roximity_beacon_1
                        RSSI = beacon.split(",")[5]
                        TX_power = beacon.split(",")[4]
                        epoch_time = time.time()
                        doc = {'pi_id': pi_id, 'beacon_id': "rox_1", 'epoch_time': epoch_time, 'MAC': mac, 'TX_power': TX_power, 'RSSI':RSSI}
                        db.save(doc)
                        print doc

		elif mac == "0c:f3:ee:0e:a5:05": #roximity_beacon_2
                        RSSI = beacon.split(",")[5]
                        TX_power = beacon.split(",")[4]
                        epoch_time = time.time()
                        doc = {'pi_id': pi_id, 'beacon_id': "rox_2", 'epoch_time': epoch_time, 'MAC': mac, 'TX_power': TX_power, 'RSSI':RSSI}
                        db.save(doc)
                        print doc
                        
		elif mac == "f7:6d:88:66:6d:30": #redbear_ble_nano_1
                        RSSI = beacon.split(",")[5]
                        TX_power = beacon.split(",")[4]
                        epoch_time = time.time()
                        doc = {'pi_id': pi_id, 'beacon_id': "rb_nano_1", 'epoch_time': epoch_time, 'MAC': mac, 'TX_power': TX_power, 'RSSI':RSSI}
                        db.save(doc)
                        print doc
                        
		elif mac == "CB:6f:40:e8:ac:5c": #redbear_ble_nano_2
			RSSI = beacon.split(",")[5]
			TX_power = beacon.split(",")[4]
                        epoch_time = time.time()
			doc = {'pi_id': pi_id, 'beacon_id': "rb_nano_2", 'epoch_time': epoch_time, 'MAC': mac, 'TX_power': TX_power, 'RSSI':RSSI}
			db.save(doc)
			print doc
			
