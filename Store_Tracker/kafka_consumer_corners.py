from kafka import KafkaConsumer
import couchdb
import time
import statistics
import json
import math
import sys
import deal_email
from queue import *


SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'blah'
COUCHDB_SERVER = 'http://52.14.61.109:5984'

last_sent_pi = None

# start new reading every X seconds
last_window_epoch = time.time()
first_reading_done = False
readings = {}

pi_locations = {
    'pi_1': (1,1),
    'pi_2': (1,0),
    'pi_3': (0,0),
    'pi_4': (0,1)
}


# processed data will be added to separate database
server = couchdb.client.Server(COUCHDB_SERVER)
db = server['processed_ble']

last_nearest_pis = Queue(maxsize=5)

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
    data = json.loads(msg[6].decode('utf-8'))

    # only track one beacon
    if data['beacon_id'] != 'rb_nano_1':
        continue

    # append rssi reading to list if list for pi id exists, otherwise create one
    if data['pi_id'] in readings:
        if readings[data['pi_id']].full():
            readings[data['pi_id']].get()
        readings[data['pi_id']].put(data['RSSI'])
    else:
        readings[data['pi_id']] = Queue(maxsize=10)
        readings[data['pi_id']].put(data['RSSI'])
     
    # do actual processing    
    smallest_rssi = 200
    closest_pi = None

    for pi_id in readings:
        median_rssi = math.fabs(statistics.mean(list(readings[pi_id].queue)))
        if median_rssi < smallest_rssi:
            smallest_rssi = median_rssi
            closest_pi = pi_id

    if closest_pi == None:
        continue

    if last_nearest_pis.full():
        last_nearest_pis.get()
    last_nearest_pis.put(closest_pi)

    all_equal = True
    for pi in list(last_nearest_pis.queue):
        if pi != closest_pi:
            all_equal = False

    if not all_equal:
        continue

    print(closest_pi, data['epoch_time'])

    if closest_pi != last_sent_pi:

        if closest_pi == 'pi_3':
            sendDealEmail()

        last_sent_pi = closest_pi

        # add processed data to database
        new_doc = {
            'location_x': pi_locations[closest_pi][0],
            'location_y': pi_locations[closest_pi][1],
            'epoch_time': last_window_epoch
        }
        db.save(new_doc)

    sys.stdout.flush()

consumer.close()
