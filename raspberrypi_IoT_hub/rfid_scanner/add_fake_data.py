import couchdb

COUCHDB_SERVER = 'http://52.14.61.109:5984'


server = couchdb.client.Server(COUCHDB_SERVER)
server.resource.credentials = ('admin','drewmeyers#1')
db = server['items']

#new_doc = couchdb.client.Document

db.save({
	'price':20,
	'uid':'0000000',
	'gid':'0000000',
	'status':'II',
	'item_Name':'MILK',
	'date_sold':'00/00/00',
	'sold_to':'creg'
})	

db.save({
	'price':50,
	'uid':'0000001',
	'gid':'0000000',
	'status':'II',
	'item_Name':'MILK',
	'date_sold':'00/00/00',
	'sold_to':'creg'})

db.save({
	'price':80,
	'uid':'0000020',
	'gid':'0000000',
	'status':'II',
	'item_Name':'MILK',
	'date_sold':'00/00/00',
	'sold_to':'creg'})	


db.save({
	'price':10,
	'uid':'0000003',
	'gid':'0000000',
	'status':'II',
	'item_Name':'MILK',
	'date_sold':'00/00/00',
	'sold_to':'creg'})	


db.save({
	'price':5,
	'uid':'0000004',
	'gid':'0000000',
	'status':'II',
	'item_Name':'MILK',
	'date_sold':'00/00/00',
	'sold_to':'creg'})	














	
