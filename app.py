from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import os


app = Flask(__name__)
mongo = PyMongo(app)


app.config['SECRET_KEY'] = os.urandom(32)
app.config['MONGO_DBNAME'] = 'mongologinexample'
app.config['MONGO_URI'] = 'mongodb+srv://new-user_31:mongo625@firstcluster0-1vctv.mongodb.net/test?retryWrites=true'


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.to_dict()['username']
    password = request.form.to_dict()['password'].encode()
    login_user = mongo.db.users.find_one({'name': username})

    if login_user is not None:
        if bcrypt.checkpw(password, login_user['password']):
            session['username'] = username
            # TODO: here should be user environment
            return redirect(url_for('main'))
        else:
            # TODO: here should be helpful & beautiful message
            return "Invalid password"
    else:
        # TODO: here should be helpful & beautiful message
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
