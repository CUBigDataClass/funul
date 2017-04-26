from kafka import KafkaConsumer
import couchdb
import time
import statistics
import json
import math
import sys
import trilateration
import itertools
from queue import *


SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'blah'
TIME_WINDOW = 5 # in seconds
COUCHDB_SERVER = 'http://13.58.9.233:5984'

# start new reading every X seconds
last_window_epoch = time.time()
first_reading_done = False
readings = {}

# the pi locations would ideally be set on the actual pis and then stored in the database.
# we are manually entering them here for demo purposes. it is time-consuming to manually
# change these values on multiple devices, especially on the school network where we cannot
# give them static ips (which also makes automation difficult)
MAX_X = 6.1976
MAX_Y = 10.2616

pi_locations = {
    'pi_1': trilateration.point(0.0,0.0),
    'pi_2': trilateration.point(0.0,MAX_Y),
    'pi_3': trilateration.point(MAX_X,MAX_Y),
    'pi_4': trilateration.point(MAX_X,0)
}

# processed data will be added to separate database
server = couchdb.client.Server(COUCHDB_SERVER)
db = server['processed_ble']

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
    data = json.loads(msg[6].decode('utf-8'))

    # only track one beacon
    if data['beacon_id'] != 'rb_nano_1':
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
            # the following formula found from trendline in excel
            distance = max(0.0052*math.fabs(median_rssi)**2-0.2365*math.fabs(median_rssi)+2.7178,0)
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
                trilateration.circle(pi_locations[pi_combo[0][0]], pi_combo[0][1]),
                trilateration.circle(pi_locations[pi_combo[1][0]], pi_combo[1][1]),
                trilateration.circle(pi_locations[pi_combo[2][0]], pi_combo[2][1])]
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
        normalized_x = max(min(median_x / MAX_X, 1), 0)
        normalized_y = max(min(median_y / MAX_Y, 1), 0)

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
