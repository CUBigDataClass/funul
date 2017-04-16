import couchdb
from random import randint
from subprocess import check_output

couch = couchdb.Server() #default/empty is localhost
db = couch['books']

localIP = check_output(['hostname', '-I'])
localIP = localIP.rstrip()

doc = {'piLocalIP': localIP}
db.save(doc)
print doc

while 1:
	fake_sensor_data = randint(0,1000)
	doc = {'fake_sensor_data': fake_sensor_data}
	db.save(doc)
	#for id in db:
		#print db[id]
	print doc
end
	