from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)


import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['MONGO_DBNAME'] = 'mongologinexample'
app.config['MONGO_URI'] = 'mongodb+srv://new-user_31:mongo625@firstcluster0-1vctv.mongodb.net/test?retryWrites=true'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('main.html')


@app.route('/login', methods=['GET','POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form.to_dict()})

    if login_user:
        login_user['password'] = bcrypt.gensalt()
        passwd = request.form.to_dict()['pass'].encode()
        hashpass = bcrypt.hashpw(passwd, bcrypt.gensalt())
        if hashpass == login_user['password']:
            session['username'] = request.form.to_dict()['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form.to_dict()})

        if existing_user is None:
            passwd = request.form.to_dict()['pass'].encode()
            hashpass = bcrypt.hashpw(passwd, bcrypt.gensalt())
            users.insert({'name': request.form.to_dict()['username'], 'password': hashpass})
            session['username'] = request.form.to_dict()['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
