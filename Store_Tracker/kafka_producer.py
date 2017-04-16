from kafka import KafkaProducer
from random import randint
import json

SERVERS = ['localhost:9092']
TOPIC= 'bluetooth_readings' # topic to be used for all trilateration procedures
ACKS = 0 # don't require any acknowledgements to consider the request complete
PI_ID = 'mypi3' # replace with unique id for each pi -- either using a command/libary or hard-coding

producer = KafkaProducer(bootstrap_servers=SERVERS, acks=ACKS)

for i in range(100):
    producer.send(TOPIC, value=json.dumps({
        'pi_id': PI_ID, 
        'rssi_reading': randint(-90, -30)
    }), key='BLUETOOTH1')
producer.close()
