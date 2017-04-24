from kafka import KafkaConsumer
import couchdb
import time
import statistics
import json
import sys
import trilateration
from queue import *


SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'blah'
TX_POWER = -63 # power received by receiver at distance of 1m
COUCHDB_SERVER = 'http://52.14.61.109:5984'


# hardcoded pi id--put in id of pi being calibrated here
PI_TO_TEST = 'pi_1'

file_rssi_median = open('calibration_median_rssi_' + PI_TO_TEST + '.csv', 'w')
file_rssi_raw = open('calibration_raw_rssi_' + PI_TO_TEST + '.csv', 'w')
file_distance = open('calibration_distance_' + PI_TO_TEST + '.csv', 'w')
file_epoch = open('calibration_epoch_' + PI_TO_TEST + 'csv', 'w')

# start new reading every X seconds
last_window_epoch = time.time()
readings = Queue(maxsize=10)

# the pi locations would ideally be set on the actual pis and then stored in the database.
# we are manually entering them here for demo purposes. it is time-consuming to manually
# change these values on multiple devices, especially on the school network where we cannot
# give them static ips (which also makes automation difficult)
pi_locations = {
    'pi_1': trilateration.point(0.0,0.0),
    'pi_2': trilateration.point(0.0,7.98),
    'pi_3': trilateration.point(7.82,7.98),
    'pi_4': trilateration.point(7.82,0)
}

# processed data will be added to separate database
server = couchdb.client.Server(COUCHDB_SERVER)
db = server['processed_ble']

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
    beacon_id = msg[5]
    data = json.loads(msg[6].decode('utf-8'))

    # throw out data if it's not coming from the pi we're calibrating
    if data['pi_id'] != PI_TO_TEST:
        continue

    # append rssi reading to list if list for pi id exists, otherwise create one
    if readings.full():
        readings.get()
    readings.put(data['RSSI'])
     
    # process data
    median_rssi = statistics.median(list(readings.queue))
    # the formula used to compute the distances is 10^((TxPower-RSSI)/20)
    # it is derived from a formula which appears in the following paper:
    # http://www.rn.inf.tu-dresden.de/dargie/papers/icwcuca.pdf
    distance = 10.0**((float(TX_POWER)-float(median_rssi))/20.0)

    print(median_rssi, distance)

    file_rssi_median.write(str(median_rssi) + ',')
    file_rssi_raw.write(str(data['RSSI']))
    file_distance.write(str(distance) + ',')
    file_epoch.write(str(data['epoch_time']) +  ',')

consumer.close()
