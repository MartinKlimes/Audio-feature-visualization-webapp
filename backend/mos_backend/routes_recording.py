from mos_backend import app, db
from mos_backend.db_models import Recording
from werkzeug.utils import secure_filename
import os
import string

from pydub import AudioSegment
from flask_jwt_extended import jwt_required, current_user
from flask import request, jsonify, send_from_directory




@app.route('/upload-audio-file', methods=['POST'])
@jwt_required()
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
            recording = Recording(filename=filename,
                                  filepath=filepath,
                                  user=user,
                                  isTrackSelected=False,
                                  isWaveform=False,
                                 )
            db.session.add(recording)
            db.session.commit()

        # return jsonify({'message': 'file succesfully uploaded'})
        return jsonify(filename)
    else:
        return jsonify({'message': 'file could not be uploaded'})


@app.route('/get-track-list', methods=['GET'])
@jwt_required()
def get_audio_file():
    user = current_user

    # path = f'./user_uploads/{user.username}'
    # records_only = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    records = Recording.query.filter_by( user=user).all()
    record_list = []
    for record in records:
        record_list.append({'id': record.id,
                            'trackName': record.filename,
                            'isTrackSelected': record.isTrackSelected,
                            'isWaveform': record.isWaveform,

                            })
    return jsonify(record_list)

@app.route('/change-track-status/<action_name>/<record_name>')
@jwt_required()
def change_track_status(action_name, record_name):
    user = current_user
    record = Recording.query.filter_by(filename=record_name, user=user).first()

    if action_name == 'isTrackSelected':
        record.isTrackSelected = not record.isTrackSelected

    if action_name == 'isWaveform':
        record.isWaveform = not record.isWaveform


    db.session.commit()
    return jsonify({'message': 'Status succesfully changed'})

@app.route('/rename-track/<record_name>/<modified_name>', methods=['GET'])
@jwt_required()
def rename_track(record_name, modified_name):
    user = current_user
    filepath = f'./user_uploads/{user.username}/'
    os.rename(filepath + record_name, filepath + modified_name)
    record = Recording.query.filter_by(filename=record_name, user=user).first()
    record.filename = modified_name
    record.filepath = filepath + modified_name
    db.session.commit()

    return jsonify({'message': 'Succesfully renamed'})

@app.route('/delete-audio-file/<record_name>', methods=['POST', 'GET'])
@jwt_required()
def delete_audio_fil(record_name):
    user = current_user
    os.remove(f'./user_uploads/{user.username}/{record_name}')
    Recording.query.filter_by(filename=record_name).delete()
    db.session.commit()
    return jsonify({'message': f'{record_name} successfully deleted'})


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
    user = current_user

    if start.isdigit():
        start = int(start)
    else:
        start = float(start)
    if end.isdigit():
        end = int(end)
    else:
        end = float(end)
    if fromBar == 'undefined':
        record_name_trimmed = f' {record_name} ({"{:.2f}".format(round(start, 2))}s - {"{:.2f}".format(round(end, 2))}s)'
    else:
        record_name_trimmed = f' - bars ({fromBar} - {toBar}) - {record_name}'

    recording_exists = Recording.query.filter_by(filename=record_name_trimmed, user=user).first()

    if not recording_exists:
        filepath = os.path.realpath(f'./user_uploads/{user.username}')
        sound = AudioSegment.from_file(f'{filepath}/{record_name}')


        extract = sound[start * 1000:end * 1000]

        # for f in os.listdir(f'./user_uploads/{user.username}/trimmed_tracks/'):
        #     os.remove(os.path.join(f'./user_uploads/{user.username}/trimmed_tracks/', f))

        filepath = f'./user_uploads/{user.username}/{record_name_trimmed}'
        extract.export(filepath)


        recording = Recording(filename=record_name_trimmed,
                              filepath=filepath,
                              user=user,
                              isTrackSelected=True,
                              isWaveform=True,
                              )
        db.session.add(recording)
        db.session.commit()

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


