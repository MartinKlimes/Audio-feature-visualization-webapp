from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from datetime import timedelta
# set static and template folders to load frontend assets and index.html file
app = Flask(__name__, static_folder='./vue/assets', template_folder='./vue')

CORS(app, resources={r'/*': {'origins': '*'}}, supports_credentials=True)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pswd123@localhost/mos-users'
# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://audio_feature_visualization_user:sEEBU4MVxEwTEn8ICKIOrbRsKYKcxveI@dpg-ch8dm55gk4q7lmplo310-a.oregon-postgres.render.com/audio_feature_visualization'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# postgresql://audio_feature_visualization_user:sEEBU4MVxEwTEn8ICKIOrbRsKYKcxveI@dpg-ch8dm55gk4q7lmplo310-a.oregon-postgres.render.com/audio_feature_visualization

db = SQLAlchemy(app)
# password hashing
bcrypt = Bcrypt(app)

# JWT
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key'
app.config["JWT_TOKEN_LOCATION"] = ['cookies']


# must be set to True in production
app.config["JWT_COOKIE_SECURE"] = True
jwt = JWTManager(app)

from mos_backend.db_models import User, Recording
from mos_backend import routes_user, routes_recording

