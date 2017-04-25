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


COUCHDB_SERVER = 'http://52.14.61.109:5984'

# processed data will be added to separate database
server = couchdb.client.Server(COUCHDB_SERVER)
db = server['local_ip']

for change in db.changes(feed='continuous', since='now'):
    print(change)
    doc = db.get(change['id'])
    print(doc)
