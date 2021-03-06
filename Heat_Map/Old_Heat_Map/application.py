"""
Demo Flask application to test the operation of Flask with socket.io

Aim is to create a webpage that is constantly updated with random numbers from a background python process.

30th May 2014
"""

# Start with a basic flask app webpage.
from flask.ext.socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event


__author__ = 'slynn'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

#turn the flask app into a socketio app
socketio = SocketIO(app)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

class RandomThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def randomNumberGenerator(self):
        """
        Generate a random number every 1 second and emit to a socketio instance (broadcast)
        Ideally to be run in a separate thread?
        """
        #infinite loop of magical random numbers
        print("Making random numbers")
        while not thread_stop_event.isSet():
            #delay(1)
            x = random()
            y = random()

            number = round(random()*10, 3)
            print (number)
            socketio.emit('newnumber', {'x':x,'y':y}, namespace='/test')
            sleep(self.delay)

    def run(self):
        self.randomNumberGenerator()

class PullerThread(Thread):
    def __init__(self):
        self.delay = 1
        super(RandomThread, self).__init__()

    def pullData(self):
        """
        Pull data from CouchDB processed_ble server
        """
        print("Pulling locations from database")

        server = couchdb.client.Server(COUCHDB_SERVER)
        server.resource.credentials = ('admin', 'drewmeyers#1')
        db = server['ble']

        for change in db.changes(feed='continuous', since='now'):
            doc = db.get(change['id'])
            socketio.emit('newnumber', {'x':doc['location_x'], 'y':doc['location_y']})
            if not thread_stop_event.isSet():
                break

    def run(self):
        self.pullData()

@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print ("Starting Thread")
        thread = PullerThread()
        thread.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
