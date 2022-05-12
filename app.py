import os
from flask import Flask, render_template, request, redirect
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
                        
db = client["users_db"]
users = db.users

@app.route('/')
def admin():
    return "Welcome to the user management system"
    

@app.route('/admin', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        datetime_now = datetime.now()
        users.insert_one({'name' : name, 'date' : datetime_now, 'group' : "not-assigned"})
        return redirect('/admin')
    else:
        return render_template('index.html',users=users.find())


@app.route('/admin/delete/<_id>')
def delete(_id):
    try:
        print(id)
        users.delete_one({'_id': ObjectId(_id)})
        return redirect('/admin')
      
    except:
        return"There was an issue deleteing existing user"


@app.route('/admin/update/<_id>', methods=['POST', 'GET'])
def update(_id):
    if request.method == 'POST':
        new_name = request.form['name']
        try:
            users.find_one_and_update({"_id": ObjectId(_id)}, 
                                 {"$set": {"name": new_name}})
            return redirect('/admin')

        except:
            return"There was an issue updating existing user"
        
    else:
        return render_template('update.html', _id = _id)


@app.route('/manager')
def group_index():
    return render_template('group_index.html',users=users.find())

@app.route('/manager/updategroup/<_id>', methods=['POST', 'GET'])
def updategroup(_id):
    if request.method == 'POST':
        new_group = request.form['name']
        try:
            users.find_one_and_update({"_id": ObjectId(_id)}, 
                                 {"$set": {"group": new_group}})
            return redirect('/manager')

        except:
            return"There was an issue updating existing user"
        
    else:
        return render_template('update-group.html', _id = _id)
      

        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    
