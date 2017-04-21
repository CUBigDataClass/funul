from kafka import KafkaConsumer
import couchdb
import time
import statistics
import json
import trilateration

SERVERS = ['http://13.58.127.253:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'test_group'
TIME_WINDOW = 5 # in seconds
TX_POWER = -65 # power received by receiver at distance of 1m
COUCHDB_SERVER = 'http://52.53.196.80:5984'


# start new reading every 3 seconds
last_window_timestamp = time.time()
readings = {}

# the pi locations would ideally be set on the actual pis and then stored in the database.
# we are manually entering them here for demo purposes. it is time-consuming to manually
# change these values on multiple devices, especially on the school network where we cannot
# give them static ips (which also makes automation difficult)
pi_locations = {
    'pi_1': trilateration.point(0,0),
    'pi_2': trilateration.point(10,0),
    'pi_3': trilateration.point(0,10),
    'pi_4': trilateration.point(10,10)
}

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
    data = json.loads(msg[6])

    # append rssi reading to list if list for pi id exists, otherwise create one
    if data['pi_id'] in readings:
        readings[data['pi_id']].append(data['rssi_reading'])
    else:
        readings[data['pi_id']] = [data['rssi_reading']]
     
    # throw out data if it's from before processing window
    if data['timestamp'] < last_window_timestamp:
        continue

    # do actual processing after every time window elapses
    if data['timestamp'] - last_window_timestamp >= TIME_WINDOW:
        median_distances = []
        for pi_id in readings:
            distances = []
            for rssi_reading in data[pi_id]:
                # the formula used to compute the distances is 10^((TxPower-RSSI)/20)
                # it is derived from a formula which appears in the following paper:
                # http://www.rn.inf.tu-dresden.de/dargie/papers/icwcuca.pdf
                distances.append(10^(TX_POWER-rssi_reading)/20)
            median_distance = statistics.median(distances)
            median_distances.append((pi_id, median_distance))
        median_distances.sort(key=lambda x: x[1])

        # use trilateration on three pis with smallest median distances
        if len(median_distances) < 3:
            continue

        circle_list = [
            trilateration.circle(pi_locations[median_distances[0][0]], median_distances[0][1]),
            trilateration.circle(pi_locations[median_distances[1][0]], median_distances[1][1]),
            trilateration.circle(pi_locations[median_distances[2][0]], median_distances[2][1])]
        computed_location = trilateration.do_trilateration(circle_list)

        server = couchdb.client.Server(COUCHDB_SERVER)

        print(computed_location.x, computed_location.y)

consumer.close()
