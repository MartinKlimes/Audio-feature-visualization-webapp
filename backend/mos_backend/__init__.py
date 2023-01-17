from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import timedelta
# set static and template folders to load frontend assets and index.html file
app = Flask(__name__, static_folder='./vue/assets', template_folder='./vue')

CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pswd123@localhost/mos-users'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

# password hashing
bcrypt = Bcrypt(app)

# JWT
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config["JWT_TOKEN_LOCATION"] = ['cookies']


# must be set to True in production
app.config["JWT_COOKIE_SECURE"] = False
jwt = JWTManager(app)

from mos_backend.db_models import User, Recording
from mos_backend import routes_user, routes_recording, routes_parameters

