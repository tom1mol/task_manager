import os
from flask import Flask, render_template, redirect, request, url_for                        #import our Flask functionality in order to set up the                                                                                                 application for use. also add additional functionality
from flask_pymongo import PyMongo                                                           #access our library here from flask_pymongo.
from bson.objectid import ObjectId                                                          #mongodb stores its data in json like format(bson)



app = Flask(__name__)                                                           #create an instance of Flask, or a Flask app.And we store it in                                                                                            the app variable here on line 3.

app.config["MONGO_DBNAME"] = 'task_manager'                                     #add the Mongo database name and the URL linking to that database
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')                     #this replaces line below and doesnt                                                                                                                   transmit username and password.                                                                                                                        connected via config vars in heroku

#app.config["MONGO_URI"] = 'mongodb+srv://shoot:<PASSWORD>@myfirstcluster-tjr5r.mongodb.net/task_manager?retryWrites=true'
            #inside brackets came from mongo atlas page-overview-connect-connect your application-short srv connection string-copy
            #change test to task_manager and <password> to our password
#line 13 functioned by having ip set to 0.0.0.0 and port set to 5000 in heroku config vars. 
                           
mongo = PyMongo(app)                                                            #instance of pymongo. add app into that with constructor method


@app.route('/')                                                                         #('/') refers to default route
@app.route('/get_tasks')                                #string called get_tasks.when app is run..default function is get_tasks because of '/''
def get_tasks():
    return render_template("tasks.html", tasks=mongo.db.tasks.find())                      
                                                                    # redirect to an existing template, which will be called tasks.hmtl. supply a tasks collection, which will be returned from making a call directly to Mongo.
                                                                    


@app.route('/add_task')                                                                                     #decorator with route '/add_task'
def add_task():
    return render_template('addtask.html',
    categories=mongo.db.categories.find())
    
    
@app.route('/insert_task', methods=["POST"])
def insert_task():
    tasks = mongo.db.tasks                                  #convert to dict so easily understood by mongo
    tasks.insert_one(request.form.to_dict())                #submitted in the form of a request object whenever we submit info to a URI/web location
    return redirect(url_for('get_tasks'))
    

@app.route('/edit_task/<task_id>')                      #edit task means edit properties associated with the task(due date, description etc)
def edit_task(task_id):              #we want to display the task on an editable form.we need to retrieve that task from the database.target the ID
    the_task = mongo.db.tasks.find_one({"_id": ObjectId(task_id)})  #find task from task collection using ID. _id is the key.
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories) #pass the task back and the categories to our edittask.html
    
    
                                                                                        #when submit clicked..want to update database with edited values
@app.route('/update_task/<task_id>', methods=["POST"])  #create route. specify HTTP method as POST(as it comes from our form)    
def update_task(task_id):                                                               #pass in task_id as its a hook into the primary key
    tasks = mongo.db.tasks
    tasks.update( {'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))
    
    
@app.route('/delete_task/<task_id>', methods=["POST"])
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})   #access task section. call remove. pass in task_id.objectId to format/parse task_id
    return redirect(url_for('get_tasks'))               #redirect to get_tasks



@app.route('/get_categories')
def get_categories():                      
    return render_template('categories.html',
    categories=mongo.db.categories.find())
    
    
@app.route('/delete_category/<category_id>', methods=["POST"])         #pass in the category_id
def delete_category(category_id):                   #create function with same name(delete_category) and pass in category_id as parameter to locate and
   mongo.db.categories.remove({'_id': ObjectId(category_id)})      #remove that category document from categories collection
   return redirect(url_for('get_categories'))
   
   
   
@app.route('/edit_category/<category_id>')  #edit_category takes viewer to an editable page. update_category will do the update. we pass category_id into 
def edit_category(category_id):             #the function. we name the function edit_category(same name as route). we pass in category_id
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)})) #overall job is to pass user to new view while obtaining category document from
                                                                            #database for editing
                                                    #category_id passed in as a parameter.used to search for that document and feed it to editcategory.html
                                                    #we get it there by pasing it over as a parameter called category
                                                                            
                                                                            
@app.route('/update_category/<category_id>', methods=['POST'])    #Pass in the category_id as a parameter for use in the update call
def update_category(category_id):
    mongo.db.categories.update(             #get categories collection from mongo
        {'_id': ObjectId(category_id)},     #identify and format the ID
        {'category_name': request.form.get('category_name')})   #pass in request object. drill into form contained in request object.refer to form item
                                                                #whose name is category_name
    return redirect(url_for('get_categories'))  #return redirect back to categories section using get_categories function

                                                                    
if __name__ == '__main__':                                                          #we set the host using OS import, environ object and get the IP.                                                                                   set the port and convert it to an integer(again using os.environ)
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')), 
        debug=True)                                                               #set debug to True as it allows changes to be picked """""up                                                                                        automatically in the browser and produce debug statements in the                                                                           case of a bug




