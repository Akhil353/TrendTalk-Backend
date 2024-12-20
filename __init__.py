from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
# BOILERPLATE CODE PROVIDED BY AP CSP TEACHER then modified to fit CPT project needs
"""
These object can be used throughout project.
1.) Objects from this file can be included in many blueprints
2.) Isolating these object definitions avoids duplication and circular dependencies
"""

# Setup of key Flask object (app)
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)

# Setup SQLAlchemy object and properties for the database (db)
dbURI = 'sqlite:///volumes/sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
SECRET_KEY = os.environ.get('SECRET_KEY') or 'eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTczNzY1NDAzOCwiaWF0IjoxNzA2MDMxNjM4fQ.rxW6oIxB9UItQCrE_TvjWW28Cm-BZs1O-BiUJJ_FrgQ'
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy()
Migrate(app, db)

# Images storage
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # supported file types
app.config['UPLOAD_FOLDER'] = 'volumes/uploads/'  # location of user uploaded content
