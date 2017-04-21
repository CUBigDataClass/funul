from kafka import KafkaProducer
from random import randint
import couchdb
import trilateration
import json
import time

SERVERS = ['http://13.58.127.253:9092']
TOPIC= 'bluetooth_readings' # topic to be used for all trilateration procedures
ACKS = 0 # don't require any acknowledgements to consider the request complete
COUCHDB_SERVER = 'http://52.53.196.80:5984'

server = couchdb.client.Server(COUCHDB_SERVER)
db = server['ble']
producer = KafkaProducer(bootstrap_servers=SERVERS, acks=ACKS)

for change in db.changes(feed='continuous'):
    doc = db.get(change.id)
    producer.send(TOPIC, value=json.dumps({
        'pi_id': doc['pi_id'],
        'rssi_reading': doc['rssi_reading'],
        'timestamp': doc['timestamp']}), key='BLUETOOTH1')

producer.close()
