from kafka import KafkaConsumer
import couchdb
import time
import statistics
import json
import sys
import trilateration
import itertools
from queue import *


SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'blah'
TIME_WINDOW = 5 # in seconds
TX_POWER = -63 # power received by receiver at distance of 1m
COUCHDB_SERVER = 'http://52.14.61.109:5984'


# start new reading every X seconds
last_window_epoch = time.time()
first_reading_done = False
readings = {}

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
    data = json.loads(msg[6].decode('utf-8'))

    # only track one beacon
    if data['beacon_id'] != 'rox_1':
        continue

    # change epoch if there is a backlog
    if not first_reading_done and data['epoch_time'] < last_window_epoch:
        last_window_epoch = data['epoch_time']

    # throw out data if it's from before processing window
    elif data['epoch_time'] < last_window_epoch:
        continue

    first_reading_done = True

    # append rssi reading to list if list for pi id exists, otherwise create one
    if data['pi_id'] in readings:
        if readings[data['pi_id']].full():
            readings[data['pi_id']].get()
        readings[data['pi_id']].put(data['RSSI'])
    else:
        readings[data['pi_id']] = Queue(maxsize=10)
        readings[data['pi_id']].put(data['RSSI'])
     
    # do actual processing after every time window elapses
    if data['epoch_time'] - last_window_epoch >= TIME_WINDOW:
        last_window_epoch = data['epoch_time']
        pi_distances = []
        for pi_id in readings:
            print(list(readings[pi_id].queue))
            median_rssi = statistics.mean(list(readings[pi_id].queue))
            # the formula used to compute the distances is 10^((TxPower-RSSI)/20)
            # it is derived from a formula which appears in the following paper:
            # http://www.rn.inf.tu-dresden.de/dargie/papers/icwcuca.pdf
            n = 2
            distance = 7*10**((float(TX_POWER)-float(median_rssi))/(10*n))
            pi_distances.append((pi_id, distance))
        pi_distances.sort(key=lambda x: x[1])

        print(pi_distances)

        # use trilateration on three pis with smallest pi distances
        if len(pi_distances) < 3:
            continue

        # process on each combination of three pis
        computed_locations_x = []
        computed_locations_y = []
        for pi_combo in itertools.combinations(pi_distances, 3):
            circle_list = [
                trilateration.circle(pi_locations[pi_distances[0][0]], pi_distances[0][1]),
                trilateration.circle(pi_locations[pi_distances[1][0]], pi_distances[1][1]),
                trilateration.circle(pi_locations[pi_distances[2][0]], pi_distances[2][1])]
            computed_location = trilateration.do_trilateration(circle_list)

            # do not consider pis without intersecting points
            if computed_location.x != 0:
                computed_locations_x.append(computed_location.x)
            if computed_location.y != 0:
                computed_locations_y.append(computed_location.y)


        # ignore data if no intersecting points are found
        if len(computed_locations_x) == 0 or len(computed_locations_y) == 0:
            continue

        # take medians of computed locations
        median_x = statistics.median(computed_locations_x)
        median_y = statistics.median(computed_locations_y)

        # normalize these results by dividing by x difference and y difference
        normalized_x = median_x / 7.82
        normalized_y = median_y / 7.98

        # add processed data to database
        new_doc = {
            'location_x': normalized_x,
            'location_y': normalized_y,
            'epoch_time': last_window_epoch
        }
        db.save(new_doc)

        print(median_x, median_y)
        sys.stdout.flush()

consumer.close()
