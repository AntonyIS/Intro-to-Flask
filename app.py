# import flask into our main file(app.py)
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os # to help use find the location of out database


####################Database Configuration here################################
basedir = os.path.abspath(os.path.dirname(__file__))

# class Config(object):
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, "projectonedb.db")#linux
#     # SQLALCHEMY_DATABASE_URI = 'sqlite:////temp/projectonedb.db'         #windows
#     # SQLALCHEMY_DATABASE_URI: defines the location of out database
#     # /home/injila-pc/PycharmProjects/Flask/PythonClass/projectone/projectonedb.db
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

####################Database Configuration here################################
# flask: module install in the virtualenv
# Flask : is a class found in the flask module

# create a flask application: serves as a server
app = Flask(__name__)
# app.config.from_object(Config) # make use of the setting inside the Config() class
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'projectonedb')#linux
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////temp/projectonedb.db' # windows
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db: an instance of our database
# SQLAlchemy(app) : wraps the app to use the database

# app: an object from the Flask class
# __name__ : means that when the app is running , this file(app.py) is the starting point

# routes: Paths to resources in our server
#@app: decorator: determine or define the role of a function(index()) defined/crreated below it

# request (client:browser)
# response ()
# C -Create
# R - Read
# U - Update
# D - Delete
users = [
    {'id':1,'name': 'Salma','language': 'javascript'},
    {'id':2,'name': 'Matthew','language': 'java'},
    {'id':3,'name': 'James','language': 'Kotlin'},
    {'id':4,'name': 'Lewis','language': 'Python'}
]

#####################Database tables here #################################

class User(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password= db.Column(db.String(255))

# To Interact with the database and table using the terminal
# db.create_all(): create table
# db.drop_all(): Delete tables

#####################Database tables here #################################

# Reading(getting data about all users)
@app.route('/') #http://127.0.0.1:2000; request
def index():
    users = Users.query.all()
    return render_template("index.html", users=users)


# @app.route('/greetings/<name>') #request "http://127.0.0.1:2000/greetings/james"
# # <name> is a varible that will store whatever name you put after: http://127.0.0.1:2000/greetings
# def greetings(name):
#     return render_template("greetings.html")

#
#
# @app.route('/getid/<int:user_id>')#request "http://127.0.0.1:2000/getid/100"
# def get_user_id(user_id):
#     # response must be: String, tuple,Response instance
#     return "{}".format(user_id)


# Reading(getting data about a single user using their id(user_id))
@app.route('/users/add', methods = ['GET', 'POST'])
def add_user():
    if request.method == 'POST':# sending from the FE
        # receive/grab data
        name = request.form.get('jina')
        programming_language = request.form.get('coding_language')

        # Store data into db:
        # create a user instance
        new_user = Users(name=name, language=programming_language)
        # add user to Users table
        db.session.add(new_user)
        # save user into the database
        db.session.commit()
        return render_template("index.html")
    else:
        return render_template('add_user.html')




@app.route('/users/<int:user_id>')
def get_user(user_id):
    for user in users:#loop through all the users in our list
        # user: single dictionary in our users list
        if user['id'] == user_id:
            user_name = user['name']
            return render_template("get_user.html", found_user= user_name)
        # if user is not found
        else:
            return "User not found"



# Update route
@app.route('/users/update/<int:user_id>',methods= ['POST', 'GET'] )
def update_user(user_id):
    # get user
    user = {}
    for user in users:  # loop through all users
        if user['id'] == user_id:  # get a user with user_id
            user=user
    # check method
    if request.method == 'POST':

            # changing the value
        update_user = {
            "name" : request.form['user_name'],
            "language" : request.form['user_language'],
        }
        # update the data
        user.update(update_user)
        return render_template("update_user.html", user=user)
    else:

        return render_template("update_user.html", user=user)


# Delete
@app.route('/users/delete/<int:user_id>', methods=['POST', 'GET'])
def delete_user(user_id):
    if request.method == 'GET':
        i = 0
        for user in users:
            if user['id'] == user_id:
                users.pop(i)
                return render_template('index.html')
            i +=1



# 200: everything is ok
# 201: data created successfuly
# 404: page not found
# 500:internal server error


@app.errorhandler(404)
def not_found(error):
    return "Kuna Shida Kwa Server: {}".format(error), 404


@app.errorhandler(500)
def internal_error(error):
    return "There is an internal server error: {}".format(error), 500




if __name__ == '__main__':
    # if app.py is the main file, run the server
    app.run(debug=True, port=5000)
    # debug= True : in development
    # debug= False : in production
    # port = 3000: is the port number for accessing this particular app
    # app.run(): is the method(function) that runs the server