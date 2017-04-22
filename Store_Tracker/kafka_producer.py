from kafka import KafkaProducer
from random import randint
import couchdb
import trilateration
import json
import time

SERVERS = ['localhost:9092']
TOPIC= 'bluetooth_readings' # topic to be used for all trilateration procedures
ACKS = 0 # don't require any acknowledgements to consider the request complete
COUCHDB_SERVER = 'http://52.15.234.53:5984'

server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.credentials = ('admin', 'drewmeyers#1')
db = server['ble']
producer = KafkaProducer(bootstrap_servers=SERVERS, acks=ACKS)

for change in db.changes(feed='continuous', since='now'):
    doc = db.get(change['id'])
    json_str = json.dumps({
        'pi_id': doc['pi_id'],
        'RSSI': int(doc['RSSI']),
        'epoch_time': doc['epoch_time']
    })
    producer.send(TOPIC, value=json_str.encode('utf-8'))
    print(json_str)

producer.close()
