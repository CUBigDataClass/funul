import couchdb

COUCHDB_SERVER = 'http://52.15.229.104:5984'


server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.credentials = ('admin','drewmeyers#1')


server.create('items')



