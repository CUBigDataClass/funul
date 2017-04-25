# Front End Documentation
The front end of Funul.io is hosted on a t2.micro EC2 instance of AWS running a flask server. Currently at peak times CPU utilization is at around 5%.

## Dependencies
All of the dependencies can be found in requirements.txt, and you should be able to install all of the dependencies by running
  
    sudo pip install -r requirements.txt
when in `/Heat_Map/`.

## Servers
### Local Development Server
To run a local instance navigate to `/Heat_Map/example/` and run 

    sudo python app_local.py
    
`app_local.py` is very similar to the `app.py` that needs to be run for production, but has a random number generator to feed data as opposed to receiving data from CouchDB as well as not porting to our AWS server. The local server hosts at `http://localhost:5000/`

### Production Server
To start a production server navigate to `/Heat_Map/example/` and run 

    sudo python app.py &
which will start the flask server in the background. To kill the server, you'll need to run 
    
    ps aux | grep python
to find all the `app.py` processes and run 

    sudo kill -9 ####
where `####` is the process number of an `app.py` process.

## Javascript
All of the Firebase Authentication information is in `/static/js/login.js`
All of the front end heatmapping logic is in `/static/js/heatmap.js` and `/static/js/application.js`
Often when changing `.js` files while a server (production or development) is running, you will need to open your browser's development console and the "Empty Cache and Hard Reload" the page.

## CSS
funul.io is not running any automated scripts for `.css` files, so when changing any CSS you should rename the `.css` file and change the reference in `index.html`
