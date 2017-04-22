import couchdb

COUCHDB_SERVER = 'http://52.15.234.53:5984'


server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.credentials = ('admin','drewmeyers#1')
db = server['inventory']
new_doc = couchdb.client.Document
db.save({
	'uid':'0000000',
	'gid':'0000000',
	'status':'II',
	'item_Name':'MILK',
	'date_sold':'00/00/00',
	'sold_to':'creg'})	
