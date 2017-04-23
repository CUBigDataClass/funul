import couchdb
#import pycouchdb
COUCHDB_SERVER = 'http://52.15.234.53:5984'

server = couchdb.client.Server(COUCHDB_SERVER)

#server = pycouchdb.Server(COUCHDB_SERVER)
server.resource.creidentials = ('admin','drewmeyes#1')

#db = server.database('local_ip')
db = server['processed_ble']
#list(("hello","byebye","hello"))

def fun(doc):
	print(doc)
	print(doc['location_x'])
	if "pi_4" == doc['pi_id']:
		return(doc)

map_func = "function(doc) {emit(doc.name, 1);}"
#print(list(db.query("function(doc) { emit(doc.i,null); }",descending=True)))
for row in db:
#	print(db.get(row))
	fun(db.get(row))
#print(h)
#list(db.temporary_query(map_func))
