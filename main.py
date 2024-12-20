import threading
# BOILERPLATE CODE PROVIDED BY AP CSP TEACHER then modified to fit CPT project needs
# import "packages" from flask
from flask import render_template,request  # import render_template from "public" flask libraries
from flask.cli import AppGroup


# import "packages" from "this" project
from __init__ import app, db, cors  # Definitions initialization
# commit test

# setup APIs
from api.user import user_api # blueprint import api definition
from api.player import player_api
from api.message import message_api
# database migrations
from model.users import initUsers
from model.players import initPlayers
from model.messages import initMessages

# setup App pages
from projects.projects import app_projects # blueprint directory import projects definition


# Initialize the SQLalchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(message_api)
app.register_blueprint(app_projects) # register app pages

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.before_request
def before_request():
    # check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4200', 'http://127.0.0.1:4200', 'https://nighthawkcoders.github.io', 'http://0.0.0.0:4200/student/', 'http://127.0.0.1:4100', 'http://127.0.0.1:8086']:
        cors._origins = allowed_origin

# create an AppGroup for custom commands
custom_cli = AppGroup('custom', help='Custom commands')

# Ddfine a command to generate data
@custom_cli.command('generate_data')
def generate_data():
    initUsers()
    initPlayers()
    initMessages()

# register the custom command group with the Flask application
app.cli.add_command(custom_cli)
        
# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    app.run(debug=True, host="0.0.0.0", port="8086")