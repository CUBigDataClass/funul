from kafka import KafkaConsumer
import datetime
import statistics
import json

SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'test_group'
TIME_WINDOW = 3 # in seconds


# start new reading every 3 seconds
last_window_timestamp = time.time()
readings = {}
tx_powers = {}
pi_locations = {}

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
	data = json.loads(msg[6])

	# write pi-specific properties to dictionary, overwriting if necessary
	tx_powers[data['pi_id']] = data['tx_powers']
	pi_locations[data['pi_id']] = data['pi_locations']

	# append rssi reading to list if list for pi id exists, otherwise create one
    if data['pi_id'] in readings:
    	readings[data['pi_id']].append(data['rssi_reading'])
    else
    	readings[data['pi_id']] = [data['rssi_reading']]

    # do actual processing after every time window elapses
    if data['timestamp'] - last_window_timestamp >= TIME_WINDOW:
    	median_distances = []
    	for pi_id in readings:
    		distances = []
    		for rssi_reading in data[pi_id]:
    			# the formula used to compute the distances is 10^((TxPower-RSSI)/20)
    			# it is derived from a formula which appears in the following paper:
    			# http://www.rn.inf.tu-dresden.de/dargie/papers/icwcuca.pdf
    			distances.append(10^(tx_powers[pi_id]-rssi_reading)/20)
    		median_distance = statistics.median(distances)
    		median_distances.append((pi_id, median_distance))
    	median_distances.sort(key=lambda x: x[1])

    	# use trilateration on three pis with smallest median distances
    	circle_list = [
    		trilateration.circle(pi_locations[median_distances[0][0]], median_distances[0][1]),
    		trilateration.circle(pi_locations[median_distances[1][0]], median_distances[1][1]),
    		trilateration.circle(pi_locations[median_distances[2][0]], median_distances[2][1])]
    	computed_location = trilateration.do_trilateration(circle_list)

    	print(computed_location.x, computed_location.y)

consumer.close()
