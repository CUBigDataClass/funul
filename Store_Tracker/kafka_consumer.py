from kafka import KafkaConsumer
import datetime
import json

SERVERS = ['localhost:9092'] # kafka server list
TOPIC = 'bluetooth_readings' # topic to be used for all trilateration procedures
GROUP_ID = 'test_group'

readings_dict = {}

consumer = KafkaConsumer(TOPIC, bootstrap_servers=SERVERS, auto_offset_reset='earliest', group_id=GROUP_ID)
for msg in consumer:
    print(json.loads(msg[6])['rssi_reading'])

consumer.close()
