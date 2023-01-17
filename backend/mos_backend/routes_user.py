from mos_backend import app, db, bcrypt, jwt
from mos_backend.db_models import User, Recording

#  from requests_toolbelt import MultipartEncoder
# import base64
# from io import BytesIO
#
# from music21 import  *
# import numpy as np
# import json

from flask import render_template
from flask import request, jsonify, send_from_directory, send_file

from werkzeug.utils import secure_filename
import os, string

# jwt auth
from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

# current user is a global variable, which can be accessed by all routes guarded by jwt
from flask_jwt_extended import current_user
from flask_jwt_extended import verify_jwt_in_request

# time
from datetime import datetime
from datetime import timedelta


# catch all the routes from Vue router (client-side routing)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')


# if the jwt is about to expire, add a new one to a given request response
@app.after_request
def refresh_expiring_jwts(response):
    try:

        exp_timestamp = get_jwt()['exp']
        now = datetime.now()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=20))
        # print(datetime.fromtimestamp(target_timestamp), datetime.fromtimestamp(exp_timestamp))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user,
                                               expires_delta=timedelta(minutes=20))
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    return User.query.filter_by(id=identity).first()


def validate_username(username):
    return User.query.filter_by(username=username).first()


def validate_email(email):
    return User.query.filter_by(email=email).first()


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username=username).first()
    if user:
        # check if the password is correct
        pw_correct = bcrypt.check_password_hash(user.password, password)
        if pw_correct:
            response = jsonify({'message': 'login successful'})

            # create access token with user from the db for later identification
            access_token = create_access_token(identity=user, expires_delta=timedelta(minutes=20))
            set_access_cookies(response=response, encoded_access_token=access_token)

            return response

        else:
            return jsonify({'message': 'wrong password'})
    else:
        return jsonify({'message': 'user does not exist'})


@app.route('/logout', methods=['POST'])
def logout():

    response = jsonify({'message': 'logout successful'})
    unset_jwt_cookies(response)
    return response


@app.route('/login-check', methods=['GET'])
@jwt_required()
def login_check():
        jwt_from_request = verify_jwt_in_request()
        if jwt_from_request is not None:
            time = get_jwt()['exp']
            return jsonify({'message': 'jwt is valid',
                            'username': current_user.username,
                            'exp': datetime.fromtimestamp(time)})
        else:
            return jsonify({'message': 'jwt is missing'})


@app.route('/register', methods=['POST'])
def register():
    username_exists = validate_username(request.json['username'])
    email_exists = validate_email(request.json['email'])
    if username_exists or email_exists:
        if username_exists and email_exists:
            return jsonify({'message': 'email and username already exist'})
        elif username_exists:
            return jsonify({'message': 'username already exists'})
        elif email_exists:
            return jsonify({'message': 'email already exists'})
    else:
        hashed_password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
        new_user = User(username=request.json['username'],
                        email=request.json['email'],
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # create folder for audio file uploads
        username = request.json['username']
        os.mkdir(f'./user_uploads/{username}')
        os.mkdir(f'./user_uploads/{username}/ground_truth')
        os.mkdir(f'./user_uploads/{username}/trimmed_tracks')
        os.mkdir(f'./user_uploads/{username}/MIDI')
        return jsonify({'message': 'registration successful'})


