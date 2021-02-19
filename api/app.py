from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create app
app = Flask(__name__)

# make database a sqlite database for now. Use MySQL for production
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

"""
To create SQLite db run the following in a python terminal
cd /api
python
>>> from app import db
>>> db.create_all()

ref: https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
"""

# create db object
db = SQLAlchemy(app)

## example user
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Rating %r>' % self.rating

@app.route('/ratebot/', methods=['GET', 'POST'])
def rate_bot():
    if request.method == 'GET':
        return jsonify({'msg': 'Only POST requests allowed. See API reference'})
    else:
        args = request.get_json()

        if args is None:
            return jsonify({'msg': 'No arguments provided'})
        
        rating = args['rating']
        user = args['user']
        msg = args['msg']

        if rating and user and msg:
            r = Rating(user=user, rating=rating, comment=msg)
            db.session.add(r)
            db.session.commit()
            return jsonify({'msg': "Bot rated succesfully"})
        else:
            return jsonify({'msg': 'Not enough arguments'})

    return jsonify({'msg', 'bot rated successfully'})


@app.route('/ratings/')
def getRatings():
    ratings = Rating.query.all()
    data = []
    for rating in ratings:
        data.append({'user': rating.user, 'msg': rating.comment, 'rating': rating.rating})
    return jsonify({'ratings': data})


## These are example routes

@app.route('/')
def index():
    return jsonify({'msg': 'Hello World!'})

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    """Content type header must be application/json """
    if request.method == 'GET':
        return jsonify({'msg': 'Only POST requests allowed. See API reference'})
    else: 
        args = request.get_json()

        if args is None:
            return jsonify({'msg': 'No arguments provided'})
        
        username = args['username']
        email = args['email']

        if username and email:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            return jsonify({'msg': 'user added'})
        
        return jsonify({'msg': 'No user added. Check the API'})


@app.route('/getusers/')
def getUsers():
    usrs = User.query.all()
    usr_list = []
    for usr in usrs:
        usr_list.append(usr.username)
    return jsonify({'users': usr_list})

@app.route('/getusername/')
def getuser():
    args = request.args
    if 'email' in args:
        email = args['email']
        usr = User.query.filter_by(email=email).first()
        return jsonify({'username': usr.username})
    elif 'id' in args:
        uid = args['id']
        usr = User.query.filter_by(id=uid).first()
        return jsonify({'username': usr.username})
    else:
        return jsonify({'msg': 'Please provide username parameter'})


@app.route('/deluser', methods=['GET', 'POST'])
def deluser():
    """Content type header must be application/json """
    if request.method == 'GET':
        return jsonify({'msg': 'Only POST requests allowed. See API reference'})
    else: 
        args = request.get_json()

        if args is None:
            return jsonify({'msg': 'No arguments provided'})

        if 'username' in args:
            User.query.filter_by(username=args['username']).delete()
            db.session.commit()
            return jsonify({'msg': 'user deleted'})
        elif 'email' in args:
            User.query.filter_by(email=args['email']).delete()
            db.session.commit()
            return jsonify({'msg': 'user deleted'})
        elif 'id' in args:
            User.query.filter_by(id=args['id']).delete()
            db.session.commit()
            return jsonify({'msg': 'user deleted'})
        
        return jsonify({'msg': 'Unable to delete user'})

if __name__ == '__main__':
    app.run(debug=True)