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
COUCHDB_SERVER = 'http://13.58.9.233:5984'

# processed data will be added to separate database
server = couchdb.client.Server(COUCHDB_SERVER)
db = server['processed_ble']

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
    print('cle')

consumer.close()
