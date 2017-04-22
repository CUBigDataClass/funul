from kafka import KafkaConsumer
import couchdb
import time
import statistics
import json
import sys
import trilateration

SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'blah'
TIME_WINDOW = 5 # in seconds
TX_POWER = -63 # power received by receiver at distance of 1m
COUCHDB_SERVER = 'http://52.15.234.53:5984'


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
    'pi_2': trilateration.point(0.5,0.0),
    'pi_3': trilateration.point(0.0,0.5),
    'pi_4': trilateration.point(0.5,0.5)
}

# processed data will be added to separate database
server = couchdb.client.Server(COUCHDB_SERVER)
db = server['processed_ble']

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
    device_id = msg[5]
    data = json.loads(msg[6].decode('utf-8'))

    # change epoch if there is a backlog
    if not first_reading_done and data['epoch_time'] < last_window_epoch:
        last_window_epoch = data['epoch_time']

    # throw out data if it's from before processing window
    elif data['epoch_time'] < last_window_epoch:
        continue

    first_reading_done = True

    # append rssi reading to list if list for pi id exists, otherwise create one
    if data['pi_id'] in readings:
        readings[data['pi_id']].append(data['RSSI'])
    else:
        readings[data['pi_id']] = [data['RSSI']]
     
    # do actual processing after every time window elapses
    if data['epoch_time'] - last_window_epoch >= TIME_WINDOW:
        last_window_epoch = data['epoch_time']
        median_distances = []
        for pi_id in readings:
            distances = []
            for rssi_reading in readings[pi_id]:
                # the formula used to compute the distances is 10^((TxPower-RSSI)/20)
                # it is derived from a formula which appears in the following paper:
                # http://www.rn.inf.tu-dresden.de/dargie/papers/icwcuca.pdf
                distances.append(10.0**((float(TX_POWER)-float(rssi_reading))/20.0))
            median_distance = statistics.median(distances)
            median_distances.append((pi_id, median_distance))
        median_distances.sort(key=lambda x: x[1])

        print(median_distances)

        # use trilateration on three pis with smallest median distances
        if len(median_distances) < 3:
            continue

        circle_list = [
            trilateration.circle(pi_locations[median_distances[0][0]], median_distances[0][1]),
            trilateration.circle(pi_locations[median_distances[1][0]], median_distances[1][1]),
            trilateration.circle(pi_locations[median_distances[2][0]], median_distances[2][1])]
        for circle in circle_list:
            print(circle.center.x, circle.center.y, circle.radius)
        computed_location = trilateration.do_trilateration(circle_list)


        # add processed data to database
        new_doc = {
            'location_x': computed_location.x,
            'location_y': computed_location.y,
            'epoch_time': last_window_epoch
        }
        db.save(new_doc)

        print(computed_location.x, computed_location.y)
        sys.stdout.flush()

consumer.close()
