from mos_backend import app, db, bcrypt, jwt
from mos_backend.db_models import User, Recording

from pydub import AudioSegment
from requests_toolbelt import MultipartEncoder
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import pretty_midi
import librosa.display
from music21 import  *
import numpy as np
import json

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
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
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


@app.route('/upload-audio-file', methods=['POST'])
# @jwt_required()
def upload_audio_file():
    user = current_user
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        filepath = f'./user_uploads/{user.username}/{filename}'
        # check if a recording already exists in the database (for a given user)
        # multiple users can upload recordings with the same filename
        recording_exists = Recording.query.filter_by(filename=filename, user=user).first()
        if not recording_exists:
            file.save(filepath)
            recording = Recording(filename=filename, filepath=filepath, user=user)
            db.session.add(recording)
            db.session.commit()

        # return jsonify({'message': 'file succesfully uploaded'})
        return jsonify(filename)
    else:
        return jsonify({'message': 'file could not be uploaded'})

@app.route('/get-track-list', methods=['POST', 'GET'])
@jwt_required()
def get_audio_file():
    user = current_user
    path = f'./user_uploads/{user.username}'
    records_only = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    return jsonify(records_only)
@app.route('/delete-audio-file/<record_name>', methods=['POST', 'GET'])
@jwt_required()
def delete_audio_fil(record_name):
    user = current_user
    os.remove(f'./user_uploads/{user.username}/{record_name}')
    Recording.query.filter_by(filename = record_name).delete()
    db.session.commit()
    return jsonify({'message': f'{record_name} succesfully deleted'})

@app.route('/get-audio-file/<record_name>')
@jwt_required()
def get_filepath(record_name):
    user = current_user
    filepath = os.path.realpath(f'./user_uploads/{user.username}')
    record_name.translate(str.maketrans('', '', string.punctuation))
    return send_from_directory(
        filepath,
        record_name,
        as_attachment=False
    )

@app.route('/send-time-annotations/<record_name>')
@jwt_required()
def send_time_annotations(record_name):
    user = current_user
    record = Recording.query.filter_by(filename=record_name, user=user).first()
    if record.ground_truth:
        return jsonify(record.ground_truth)


@app.route('/upload-text-file/<record_name>', methods=['POST'])
@jwt_required()
def upload_text_file(record_name):
    user = current_user
    record = Recording.query.filter_by(filename=record_name, user=user).first()
    if request.files:
        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = f'./user_uploads/{user.username}/ground_truth/{filename}'
        file.save(filepath)
        record.ground_truth = filepath
        db.session.commit()
    else:
        filepath = record.ground_truth

    lines = []

    if filepath:
        f = open(filepath, 'r')
        for line in f:
            lines.append(line.strip())
    return jsonify(lines)
@app.route('/trim-audio/<record_name>/<start>/<end>/<fromBar>/<toBar>', methods=['POST', 'GET'])
@jwt_required()
def trim_audio(record_name, start, end, fromBar, toBar):
    print(fromBar)
    user = current_user
    filepath = os.path.realpath(f'./user_uploads/{user.username}')
    sound = AudioSegment.from_file(f'{filepath}/{record_name}')
    if start.isdigit():
        start = int(start)
    else:
        start = float(start)
    if end.isdigit():
        end = int(end)
    else:
        end = float(end)

    extract = sound[start*1000:end*1000]
    if fromBar == 'undefined':
        record_name_trimmed = f' - trimmed ({"{:.2f}".format(round(start,2))}s - {"{:.2f}".format(round(end,2))}s) - {record_name}'
        print('trimmed')
        print(record_name_trimmed)
    else:
        record_name_trimmed = f' - bars ({fromBar} - {toBar}) - {record_name}'
        print('bars')
        print(record_name_trimmed)
    # for f in os.listdir(f'./user_uploads/{user.username}/trimmed_tracks/'):
    #     os.remove(os.path.join(f'./user_uploads/{user.username}/trimmed_tracks/', f))

    filepath = f'./user_uploads/{user.username}/trimmed_tracks/{record_name_trimmed}'
    extract.export(filepath)
    return jsonify(f'{record_name_trimmed} was succesfuly trimmed!')

@app.route('/get-trimmed-audio/<record_name>', methods=['POST', 'GET'])
@jwt_required()
def get_trimmed_audio(record_name):
    print(record_name)

    user = current_user

    return send_from_directory(
        os.path.realpath(f'./user_uploads/{user.username}/trimmed_tracks/'),
        record_name,
        as_attachment=False, environ=request.environ
    )

@app.route('/get-midi', methods=[ 'POST'])
@jwt_required()
def get_midi():

    user = current_user
    file = request.files['file']

    if file:
        filename = secure_filename(file.filename)
        filepath_midi = f'./user_uploads/{user.username}/MIDI/{filename}'
        file.save(filepath_midi)

    #     # MIDI_exists = Recording.query.filter_by(filename=filename, user=user).first()
    #     # if not MIDI_exists:
    #     #     file.save(filepath_midi)
    #     #     MIDI = Recording(filename=filename, filepath=filepath_midi, user=user)
    #     #     db.session.add(MIDI)
    #     #     db.session.commit()
    # # user = current_user
    # # filepath_midi = os.path.realpath(f'./user_uploads/{user.username}/MIDI/data_midi_chopin_01.mid')
    #
    # if pm:
    #
    #     def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
    #         # Use librosa's specshow function for displaying the piano roll
    #         librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
    #                                  hop_length=1, sr=fs, x_axis='time', y_axis='cqt_note',
    #                                  fmin=pretty_midi.note_number_to_hz(start_pitch))
    #     plt.figure(figsize=(40, 3))
    #     plt.axis('off')
    #
    #     # fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    #     plot_piano_roll(pm, 24, 100)
    #     # ymin, ymax = plt.ylim()
    #
    #     # Plot beats as grey lines, downbeats as white lines
    #     # mir_eval.display.events(beats, base=ymin, height=ymax, color='#AAAAAA')
    #     # mir_eval.display.events(downbeats, base=ymin, height=ymax, color='#FFFFFF', lw=2)
    #     # Only display 20 seconds for clarity
    #     # plt.xlim();
    #     filepath_pianoroll = os.path.realpath(f'./user_uploads/{user.username}/MIDI/pianoroll.png')
    #     plt.savefig(filepath_pianoroll, bbox_inches = 'tight',
    # pad_inches = 0)
    #     image = os.path.realpath(f'./user_uploads/{user.username}/MIDI/pianoroll.png')
    #     return send_file(image, mimetype='image/png')
    return jsonify(f'{filename} was succesfuly uploaded!')




@app.route('/get-pianoroll/<start>/<end>/', methods=[ 'GET', 'POST'])
@jwt_required()
def get_pianoroll(start, end):
    user = current_user




    filepath_midi = os.path.realpath(f'./user_uploads/{user.username}/MIDI/data_midi_chopin_01.mid')
    pm = pretty_midi.PrettyMIDI(filepath_midi)

    def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
        # Use librosa's specshow function for displaying the piano roll
        librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
                                 hop_length=1, sr=fs, x_axis='time', y_axis='cqt_note',
                                 fmin=pretty_midi.note_number_to_hz(start_pitch))

    plt.figure(figsize=(83.83, 3))
    plt.axis('off')

    # fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    plot_piano_roll(pm, 24, 100)
    if (start != 'undefined') and (end != 'undefined'):
        if start.isdigit():
            start = int(start)
        else:
            start = float(start)
        if end.isdigit():
            end = int(end)
        else:
            end = float(end)
        plt.xlim(start, end);

    filepath_pianoroll = os.path.realpath(f'./user_uploads/{user.username}/MIDI/pianoroll.png')
    plt.savefig(filepath_pianoroll, bbox_inches='tight',
                pad_inches=0)
    image = os.path.realpath(f'./user_uploads/{user.username}/MIDI/pianoroll.png')
    return send_file(filepath_pianoroll, mimetype='image/png')




@app.route('/get-onset-detection/<record_name>')
@jwt_required()
def get_onset_detection(record_name):
    user = current_user

    if ' - trimmed (' in record_name or ' - bars (' in record_name:
        y, sr = librosa.load(f'./user_uploads/{user.username}/trimmed_tracks/{record_name}')
    else:
        y, sr = librosa.load(f'./user_uploads/{user.username}/{record_name}')

    onset = librosa.onset.onset_detect(y, sr=sr, units='time')
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')



    onset_lists = onset.tolist()
    beats_lists = beats.tolist()
    list = onset_lists, beats_lists
    json_str = json.dumps(list)
    return json_str

# @app.route('/get-spectrogram', methods=[ 'GET', 'POST'])
# @jwt_required()
# def get_spectrogram():
#     user = current_user
#     plt.rcParams["figure.figsize"] = [81.53, 3.2]
#     plt.rcParams["figure.autolayout"] = True
#
#     fig, ax = plt.subplots()
#     plt.axis('off')
#     # Loading demo track
#     y, sr = librosa.load(os.path.realpath(f'./user_uploads/{user.username}/chopin_01.mp3'))
#
#     S = librosa.feature.melspectrogram(y=y, sr=sr, fmax=8000)
#     S_dB = librosa.power_to_db(S, ref=np.max)
#     img = librosa.display.specshow(S_dB, x_axis='time', y_axis='mel', sr=sr, fmax=8000, ax=ax)
#
#     filepath_spectrogram = os.path.realpath(f'./user_uploads/{user.username}/spectrogram.png')
#     plt.savefig(filepath_spectrogram, bbox_inches='tight',
#                 pad_inches=0)
#     return send_file(filepath_spectrogram, mimetype='image/png')