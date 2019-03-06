import os
from flask import Flask, render_template, redirect, request, url_for    #import our Flask functionality in order to set up the                                                                         application for use. also add additional functionality
from flask_pymongo import PyMongo                                       #access our library here from flask_pymongo.
from bson.objectid import ObjectId                                      #mongodb stores its data in json like format(bson)



app = Flask(__name__)                       #create an instance of Flask, or a Flask app.And we store it in the app variable here                                                  on line 3.

app.config["MONGO_DBNAME"] = 'task_manager'     #add the Mongo database name and the URL linking to that database
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')                     #this replaces line below


#app.config["MONGO_URI"] = 'mongodb+srv://shoot:<PASSWORD>@myfirstcluster-tjr5r.mongodb.net/task_manager?retryWrites=true'
            #inside brackets came from mongo atlas page-overview-connect-connect your application-short srv connection string-copy
            #change test to task_manager and <password> to our password
#line 14 functioned by having ip set to 0.0.0.0 and port set to 5000 in heroku config vars. 
                           
mongo = PyMongo(app)                                                #instance of pymongo. add app into that with constructor method


@app.route('/')                                                     #('/') refers to default route
@app.route('/get_tasks')                    #string called get_tasks.when app is run..default function is get_tasks because of '/''
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())   #.tasks is collection. find method returns everything in                                                                   tasks collection
                                                                    # redirect to an existing template, which will be called tasks.hmtl. supply a tasks collection, which will be returned from making a call directly to Mongo.
if __name__ == '__main__':                                      #we set the host using OS import, environ object and get the IP.                                                                set the port and convert it to an integer(again using os.environ)
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')), 
        debug=True)                                             #set debug to True as it allows changes to be picked up                                                                automatically in the browser and produce debug statements in the                                                       case of a bug






"""
MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "task_manager"
COLLECTION_NAME = "categories"

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("could not connect to MongoDB: %s") % e
        
"""


"""
import os
from flask import Flask, render_template, redirect, request, url_for    #import our Flask functionality in order to set up the          application for use. also add additional functionality
from flask_pymongo import PyMongo       #access our library here from flask_pymongo.
from bson.objectid import ObjectId      #mongodb stores its data in json like format(bson)
import pymongo

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "task_manager"
COLLECTION_NAME = "categories"

def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("Mongo is connected!")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("could not connect to MongoDB: %s") % e
        
conn = mongo_connect(MONGODB_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]

doccuments = coll.find()

for doc in documents:
    print(doc)


"""

"""
So you can do in your app.py file 
MONGO_URI=os.environ.get('MONGO_URI') 
And then on heroku in the settings tab 
for the app you can set a config var called MONGO_URI the value of which is the MONGO_URI connection string.


"""