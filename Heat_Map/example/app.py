#!/usr/bin/env python
from flask import Flask, render_template, session, request, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from random import random
import couchdb
from flask_bootstrap import Bootstrap
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
Bootstrap(app)
'''
def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
    	x = random()
	y = random()

	count += 1
        socketio.emit('newnumber',
                      {'x':x, 'y':y},
                      namespace='/test')
'''
COUCHDB_SERVER = 'http://52.14.61.109:5984'
def background_thread():
    """Example of how to send server generated events to clients."""

    while True:
        server = couchdb.client.Server(COUCHDB_SERVER)
	server.resource.credentials = ('admin', 'drewmeyers#1')
	db = server['processed_ble']
	for change in db.changes(feed = 'continuous', since='now'):
		doc = db.get(change['id'])
		print("here")
		x_loc = doc['location_x']
		y_loc = doc['location_y']
		print(x_loc)
		socketio.emit('newnumber',{'x':x_loc,'y':y_loc},namespace='/test')
		#if not thread_stop_event.isSet():
		#	break

#url_for('static', filename='style.css')
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    '''emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)
'''
@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    '''emit('my_response', {'data': 'Connected', 'count': 0})
'''

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port = 80)
