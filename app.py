# import flask into our main file(app.py)
from flask import Flask, render_template
# flask: module install in the virtualenv
# Flask : is a class found in the flask module

# create a flask application: serves as a server
app = Flask(__name__)
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

# Reading(getting data about all users)
@app.route('/') #http://127.0.0.1:2000; request
def index():
    return render_template("index.html", watu=users)


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
@app.route('/users/update/<int:user_id>')
def update_user(user_id):
    for user in users:#loop through all users
        if user['id']  == user_id: #get a user with user_id
            return render_template("update_user.html", user=user)




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