import couchdb

COUCHDB_SERVER = 'http://52.53.196.80:5984'


server = couchdb.client.Server(COUCHDB_SERVER)
#server.resource.credentials = ('admin','drewmeyers#1')
db = server['items']

#new_doc = couchdb.client.Document

db.save({
	'price':5,
	'gid':'E2 00 51 86 01 07 01 88 21 10 3A 93',
	'uid':'0000000',
	'status':'II',
	'item_Name':'MILK',
	'date_sold':'00/00/00',
	'sold_to':'creg'
})

db.save({
	'price':50,
	'gid':'E2 00 51 86 01 07 01 88 20 70 3D 5F',
	'uid':'0000000',
	'status':'II',
	'item_Name':'GIZZARDS',
	'date_sold':'00/00/00',
	'sold_to':'creg'})

db.save({
	'price':10,
	'gid':'53 75 73 68 69 21 01 88 07 90 C4 BF',
	'uid':'0000000',
	'status':'II',
	'item_Name':'PANTS',
	'date_sold':'00/00/00',
	'sold_to':'creg'})


db.save({
	'price':10,
	'gid':'68 65 6C 6C 6F 21 01 88 07 60 C9 B8',
	'uid':'0000000',
	'status':'II',
	'item_Name':'BANANAS',
	'date_sold':'00/00/00',
	'sold_to':'creg'})


db.save({
	'price':90,
	'gid':'4D 69 6C 6B 01 07 01 88 07 70 C4 BD',
	'uid':'0000000',
	'status':'II',
	'item_Name':'CROCS',
	'date_sold':'00/00/00',
	'sold_to':'creg'})

db.save({
	'price':2,
	'gid':'E2 00 51 86 01 07 01 88 08 00 C4 C0',
	'uid':'0000000',
	'status':'II',
	'item_Name':'MTDEW',
	'date_sold':'00/00/00',
	'sold_to':'creg'})

db.save({
	'price':15,
	'gid':'E2 00 51 86 01 07 01 88 21 00 3A 92',
	'uid':'0000000',
	'status':'II',
	'item_Name':'SNAKEOIL',
	'date_sold':'00/00/00',
	'sold_to':'creg'})

db.save({
	'price':3,
	'gid':'48 65 6C 6C 6F 21 01 88 07 80 C4 BE',
	'uid':'0000000',
	'status':'II',
	'item_Name':'APPLES',
	'date_sold':'00/00/00',
	'sold_to':'creg'})

db.save({
	'price':55,
	'gid':'E2 00 51 86 01 07 01 88 20 80 3D 60',
	'uid':'0000000',
	'status':'II',
	'item_Name':'WHITEMEAT',
	'date_sold':'00/00/00',
	'sold_to':'creg'})

db.save({
	'price':19,
	'gid':'E2 00 51 86 01 07 01 88 20 90 3A 91',
	'uid':'0000000',
	'status':'II',
	'item_Name':'TADPOLES',
	'date_sold':'00/00/00',
	'sold_to':'creg'})















