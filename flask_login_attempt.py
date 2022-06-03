import json
import logging
logging.basicConfig(level=logging.INFO)
from flask import Flask, g, request, jsonify, render_template, redirect
from flask_login import (current_user, LoginManager,
                             login_user, logout_user,
                             login_required)
from flask_mongoengine import MongoEngine
from mongoengine import *
from matplotlib import collections
app = Flask(__name__)
#mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[defaultauthdb][?options]]
#connect(host="mongodb://localhost:27017/web_application_login")
app.config['MONGODB_SETTINGS'] = {
    'db': 'web_application_login',
    'host': 'localhost',
    'port': 27017
}
app.secret_key = 'some key'
db = MongoEngine()
login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
#collection =  db['users']

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

@app.route('/login', methods=['POST'])
def login():
    # info = json.loads(request.data)
    # name = info.get('name', 'guest')
    # password = info.get('password', '')
    name = request.form['name']
    password = request.form['password']
    # info = request.get_json()
    # name = info.get('name', 'guest')
    # password = info.get('password', '')
    user = User.objects(name=name,
                        password=password).first()
    if user:
        print()
        login_user(user)
        return redirect("/logged_in")
        # return jsonify(user.to_json())
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})
 
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(**{'result': 200,
                      'data': {'message': 'logout success'}})

@app.route('/user_info', methods=['POST'])
def user_info():
    if current_user.is_authenticated:
        resp = {"status": 200,
                "data": current_user.to_json()}
    else:
        resp = {"status": 401,
                "data": {"message": "user no login"}}
    return jsonify(resp)

class User(db.Document):
    meta = {'collection': 'User'}
    name = db.StringField()
    password = db.StringField()
    email = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "email": self.email}
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)

class Job():
    def __init__(self, job_description, fcs_files, qc_files, normalize_files, normalize_graph, downsample_files, ):
        self.job_description = job_description
    def add_fcs(self):
        self.fcs_files
        return 42
    def get_fcs_names(self):
        self.fcs_files
        return 42


class UserData(db.Document):
    def __init__(self, username, email):
        self.username = username
        self.email = email
    def create_new_job():
        return True
    def get_jobList():
        return True
    def get_jobList():
        return True


@app.route('/')
def opening_page():
    return render_template("opening_page.html")

@app.route('/logged_in')
def logged_in():
    return render_template("logged_in.html")

@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    user = User.objects(name=name).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/', methods=['PUT'])
@login_required
def create_record():
    print("hiiiiiii")
    record = json.loads(request.data)
    user = User(name=record['name'],
                password=record['password'],
                email=record['email'])
    user.save()
    #collection.insert_one(user)
    #logging.info("trying to create login")
    return jsonify(user.to_json())

@app.route('/', methods=['POST'])
@login_required
def update_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(email=record['email'],
                    password=record['password'])
    return jsonify(user.to_json())

@app.route('/', methods=['DELETE'])
@login_required
def delete_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())



if __name__ == "__main__":
    app.run(port=8080, debug=True)


