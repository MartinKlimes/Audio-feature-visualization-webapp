from mos_backend import app, db
from mos_backend.db_models import Recording, Waveform, Spectrogram, Pianoroll
from werkzeug.utils import secure_filename
import os
import string

from sqlalchemy.orm import joinedload
from pydub import AudioSegment
from flask_jwt_extended import jwt_required, current_user
from flask import request, jsonify, send_from_directory, send_file

@app.route('/upload-audio-file/<file_type>', methods=['POST'])
@jwt_required()
def upload_audio_file(file_type):
    user = current_user
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        if file_type in ['audio,mpeg', 'audio,x-m4a', 'audio,wav', 'audio,flac']:
            filepath = f'./user_uploads/{user.username}/{filename}'
            # check if a recording already exists in the database (for a given user)
            # multiple users can upload recordings with the same filename
            recording_exists = Recording.query.filter_by(filename=filename, user=user).first()
            if not recording_exists:
                file.save(filepath)
                recording = Recording(filename=filename, filepath=filepath, user_id=user.id)
                db.session.add(recording)
                db.session.commit()
        elif file_type == 'text,plain':
            filepath = f'./user_uploads/{user.username}/ground_truth/{filename}'
            file.save(filepath)
        elif file_type == 'audio,mid':
            filepath = f'./user_uploads/{user.username}/MIDI/{filename}'
            file.save(filepath)
        return jsonify({'message': 'file succesfully uploaded'})
    else:
        return jsonify({'message': 'file could not be uploaded'})


@app.route('/get-track-list', methods=['GET'])
@jwt_required()
def get_audio_file():
    user = current_user
    ground_truth_path = f'./user_uploads/{user.username}/ground_truth'
    midi_path = f'./user_uploads/{user.username}/MIDI'

    recordings = Recording.query.options(
        joinedload(Recording.waveform),
        joinedload(Recording.spectrogram),
        joinedload(Recording.pianoroll)).filter_by(user=user).all()

    record_list = [recording.to_dict() for recording in recordings]


    return jsonify(record_list, os.listdir((ground_truth_path)), os.listdir((midi_path)))

@app.route('/update-recording', methods=['POST'])
@jwt_required()
def update_recording():
    data = request.get_json()
    column = data.get('column')
    new_value = data.get('new_value')
    record_id = data.get('record_id')

    user = current_user
    recording = Recording.query.filter_by(id=record_id, user=user).first()
    waveform = Waveform.query.filter_by(recording_id=recording.id).first()
    spectrogram = Spectrogram.query.filter_by(recording_id=recording.id).first()
    pianoroll = Pianoroll.query.filter_by(recording_id=recording.id).first()
    if not recording:
        return "Nahrávka nenalezena"

    setattr(recording, column, new_value)
    db.session.commit()

    if waveform:
        setattr(waveform, column, new_value)
        db.session.commit()
    if spectrogram:
        setattr(spectrogram, column, new_value)
        db.session.commit()
    if pianoroll:
        setattr(pianoroll, column, new_value)
        db.session.commit()


    return 'Status succesfully changed'

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

@app.route('/delete-audio-file/<type>/<event_name>', methods=['POST', 'GET'])
@jwt_required()
def delete_audio_fil(event_name, type):
    user = current_user

    if type == 'audio':
        record = Recording.query.filter_by(filename=event_name).first()
        print(record)
        waveform = Waveform.query.filter_by(recording_id=record.id).first()
        pianoroll = Pianoroll.query.filter_by(recording_id=record.id).first()
        spectrogram = Spectrogram.query.filter_by(recording_id=record.id).first()
        db.session.delete(waveform)
        db.session.delete(pianoroll)
        db.session.delete(spectrogram)
        os.remove(f'./user_uploads/{user.username}/{event_name}')
        db.session.delete(record)
    elif type == 'bars':
        os.remove(f'./user_uploads/{user.username}/ground_truth/{event_name}')
        records = Recording.query.filter_by(txtFileName=event_name).all()
        for record in records:
            record.txtFileName = None

    elif type == 'midi':
        os.remove(f'./user_uploads/{user.username}/MIDI/{event_name}')
        records = Recording.query.filter_by(MIDIFileName=event_name).all()
        for record in records:
            record.MIDIFileName = None

    db.session.commit()

    return jsonify({'message': f'{event_name} successfully deleted'})


@app.route('/get-file/<record_name>')
@jwt_required()
def get_filepath(record_name):
    user = current_user
    if record_name.endswith('.txt'):
        filepath = os.path.realpath(f'./user_uploads/{user.username}/ground_truth')
    elif record_name.endswith('.mid'):
        filepath = os.path.realpath(f'./user_uploads/{user.username}/MIDI')

    else:
        filepath = os.path.realpath(f'./user_uploads/{user.username}')

    record_name.translate(str.maketrans('', '', string.punctuation))
    return send_from_directory(
        filepath,
        record_name,
        as_attachment=False
    )

@app.route('/trim-audio', methods=['POST'])
@jwt_required()
def trim_audio():
    user = current_user
    record_name = request.form['record_name']
    start = request.form['start']
    end = request.form['end']
    fromBar = request.form['fromBar']
    toBar = request.form['toBar']

    if start.isdigit():
        start = int(start)
    else:
        start = float(start)
    if end.isdigit():
        end = int(end)
    else:
        end = float(end)

    if fromBar is not None:
        record_name_trimmed = f' {record_name} ({"{:.2f}".format(round(start, 2))} - {"{:.2f}".format(round(end, 2))})'
    else:

        record_name_trimmed = f' {record_name} - bars ({fromBar} - {toBar})'

    recording_exists = Recording.query.filter_by(filename=record_name_trimmed, user=user).first()
    record = Recording.query.filter_by(filename=record_name, user=user).first()
    if not recording_exists:
        filepath = os.path.realpath(f'./user_uploads/{user.username}')
        sound = AudioSegment.from_file(f'{filepath}/{record_name}')


        extract = sound[start * 1000:end * 1000]

        # for f in os.listdir(f'./user_uploads/{user.username}/trimmed_tracks/'):
        #     os.remove(os.path.join(f'./user_uploads/{user.username}/trimmed_tracks/', f))

        filepath = f'./user_uploads/{user.username}/{record_name_trimmed}'
        extract.export(filepath)

        recording = Recording(filename=record_name_trimmed, filepath=filepath, isTrackSelected=True, user_id=user.id)
        db.session.add(recording)
        db.session.commit()


    return jsonify({'message': f'{record_name_trimmed} was succesfuly trimmed!', 'id': recording.id})


# @app.route('/get-trimmed-audio/<record_name>', methods=['POST', 'GET'])
# @jwt_required()
# def get_trimmed_audio(record_name):
#     print(record_name)
#
#     user = current_user
#
#     return send_from_directory(
#         os.path.realpath(f'./user_uploads/{user.username}/trimmed_tracks/'),
#         record_name,
#         as_attachment=False, environ=request.environ
#     )

@app.route('/get-click-audio/<record_name>')
def get_click_audio(record_name):
    return send_file(os.path.realpath(f'./user_uploads/clickSound/{record_name}'))
@app.route('/get-click-audio-list')
def get_click_audio_list():
    return jsonify(os.listdir((os.path.realpath(f'./user_uploads/clickSound/'))))

