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
def main():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form.to_dict()})

    if login_user:
        login_user['password'] = bcrypt.gensalt()
        passwd = request.form.to_dict()['pass'].encode()
        hashpass = bcrypt.hashpw(passwd, bcrypt.gensalt())
        if hashpass == login_user['password']:
            session['username'] = request.form.to_dict()['username']
            return redirect(url_for('/'))
    else:
        return 'Invalid username/password combination'


@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_post():
    username = request.form.to_dict()['username']
    password = request.form.to_dict()['password'].encode()
    existing_user = mongo.db.users.find_one({'username': username})

    if existing_user is None:
        hash = bcrypt.hashpw(password, bcrypt.gensalt())
        mongo.db.users.insert({'name': username, 'password': hash})
        session['username'] = username
        # TODO: here should be template for logged-in user
        return redirect(url_for('main'))
    else:
        return 'That username already exists!'


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
