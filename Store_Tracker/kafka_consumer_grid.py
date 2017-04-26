from kafka import KafkaConsumer
import couchdb
import time
import statistics
import json
import math
import sys
import itertools
from queue import *


SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'blah'
TIME_WINDOW = 2 # in seconds
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
    'pi_1': (0.0,0.0),
    'pi_2': (0.0,MAX_Y),
    'pi_3': (MAX_X,MAX_Y),
    'pi_4': (MAX_X,0)
}

# decompose this rectangle into a grid with test points at the center of each grid square
NUM_X = 4
NUM_Y = 4

test_points = []
for i in range(NUM_X):
    x = (MAX_X/NUM_X)*(i+0.5)
    for j in range(NUM_Y):
        y = (MAX_Y/NUM_Y)*(j+0.5)

        test_points.append((x,y))

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
            distance = min(max(0.0052*math.fabs(median_rssi)**2-0.2365*math.fabs(median_rssi)+2.7178,0), min(MAX_X, MAX_Y))
            pi_distances.append((pi_id, distance))
        pi_distances.sort(key=lambda x: x[1])

        print(pi_distances)

        # use trilateration on three pis with smallest pi distances
        if len(pi_distances) < 3:
            continue

        # iterate over test points and find point with smallest error
        min_error = float('Inf')
        best_test_point = None
        for test_point in test_points:
            error = 0
            for pi_distance in pi_distances:
                pi_location = pi_locations[pi_distance[0]]
                distance_diff =  math.sqrt((test_point[0]-pi_location[0])**2+(test_point[1]-pi_location[1])**2)
                error += (distance-distance_diff)**2
            if error < min_error:
                min_error = error
                best_test_point = test_point


        if best_test_point is None:
            print('No valid test point')
            continue


        # normalize these results by dividing by x difference and y difference
        normalized_x = best_test_point[0] / MAX_X
        normalized_y = best_test_point[1] / MAX_Y

        # add processed data to database
        new_doc = {
            'location_x': normalized_x,
            'location_y': normalized_y,
            'epoch_time': last_window_epoch
        }
        db.save(new_doc)

        print(best_test_point)
        sys.stdout.flush()

consumer.close()
