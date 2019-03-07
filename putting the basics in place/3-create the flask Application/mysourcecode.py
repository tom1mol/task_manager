import os
from flask import Flask         #import our Flask functionality in order to set up the application for use

app = Flask(__name__)           #create an instance of Flask, or a Flask app.And we store it in the app variable here                                  on line 3.


@app.route('/')                 #('/') refers to default route
def hello():
    return 'Hello World...again'
    
if __name__ == '__main__':      #we set the host using OS import, environ object and get the IP. set the port and                                     convert it to an integer(again using os.environ)
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')), 
        debug=True)                         #set debug to True as it allows changes tp be picked up automatically in                                      the browser and produce debug statements in the case of a bug
