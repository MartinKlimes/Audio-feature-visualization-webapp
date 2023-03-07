from mos_backend import app, db
from mos_backend.db_models import Recording, Waveform, Spectrogram, Pianoroll
from werkzeug.utils import secure_filename
import os
import string

from pydub import AudioSegment
from flask_jwt_extended import jwt_required, current_user
from flask import request, jsonify, send_from_directory
import librosa
import librosa.display

import numpy as np

import matplotlib.pyplot as plt


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

                recording = Recording(filename=filename, filepath=filepath,isTrackSelected=False, user_id=user.id)
                db.session.add(recording)
                db.session.commit()

                # vytvoření nového záznamu v třídě Waveform
                waveform = Waveform(isWaveform=False, isWaveformDisplayed=False, waveformColor="violet, purple", recording_id=recording.id)
                db.session.add(waveform)
                db.session.commit()

                # vytvoření nového záznamu v třídě Spectrogram
                spectrogram = Spectrogram(isSpectrogram=False, isSpectrogramDisplayed=False, spectrogramColormap="jet",
                                          spectrogramHeight=256, recording_id=recording.id)
                db.session.add(spectrogram)
                db.session.commit()

                # vytvoření nového záznamu v třídě Pianoroll
                pianoroll = Pianoroll(isPianoroll=False, isPianorollDisplayed=False, pianorollColor=None,
                                      pianorollHeight=128, recording_id=recording.id)
                db.session.add(pianoroll)
                db.session.commit()
            # return jsonify({'message': 'file succesfully uploaded'})
            return jsonify(filename)

        elif file_type == 'text,plain':
            filepath = f'./user_uploads/{user.username}/ground_truth/{filename}'
            file.save(filepath)
            return jsonify(filename)

        elif file_type == 'audio,mid':
            filepath = f'./user_uploads/{user.username}/MIDI/{filename}'
            file.save(filepath)
            return jsonify(filename)

    else:
        return jsonify({'message': 'file could not be uploaded'})


@app.route('/get-track-list', methods=['GET'])
@jwt_required()
def get_audio_file():

    user = current_user
    ground_truth_path = f'./user_uploads/{user.username}/ground_truth'
    midi_path = f'./user_uploads/{user.username}/MIDI'
    recordings = Recording.query.filter_by(user=user).all()


    record_list = []
    for recording in recordings:
        waveform = Waveform.query.filter_by(recording_id=recording.id).first()
        spectrogram = Spectrogram.query.filter_by(recording_id=recording.id).first()
        pianoroll = Pianoroll.query.filter_by(recording_id=recording.id).first()

        record_list.append({
            'id': recording.id,
            'trackName': recording.filename,
            'filepath': recording.filepath,
            'ground_truth': recording.ground_truth,
            'isTrackSelected': recording.isTrackSelected,
            'backgroundColor': recording.backgroundColor,
            'txtFileName': recording.txtFileName,
            'MIDIFileName': recording.MIDIFileName,
            'splitChannels': recording.splitChannels,
            'waveform': {
                'id': waveform.id,
                'isWaveform': waveform.isWaveform,
                'isWaveformDisplayed': waveform.isWaveformDisplayed,
                'waveformColor': waveform.waveformColor,
                'waveformHeight': waveform.waveformHeight
            } if waveform else {},
            'spectrogram': {
                'id': spectrogram.id,
                'isSpectrogram': spectrogram.isSpectrogram,
                'isSpectrogramDisplayed': spectrogram.isSpectrogramDisplayed,
                'spectrogramColormap': spectrogram.spectrogramColormap,
                'spectrogramHeight': spectrogram.spectrogramHeight
            } if spectrogram else {},
            'pianoroll': {
                'id': pianoroll.id,
                'isPianoroll': pianoroll.isPianoroll,
                'isPianorollDisplayed': pianoroll.isPianorollDisplayed,
                'pianorollColor': pianoroll.pianorollColor,
                'pianorollHeight': pianoroll.pianorollHeight
            } if pianoroll else {}
        })

    return jsonify(record_list, os.listdir((ground_truth_path)), os.listdir((midi_path)))

@app.route('/update-recording', methods=['POST'])
@jwt_required()
def update_recording():
    data = request.get_json()
    record_name = data.get('record_name')
    column = data.get('column')
    new_value = data.get('new_value')


    user = current_user
    recording = Recording.query.filter_by(filename=record_name, user=user).first()
    waveform = Waveform.query.filter_by(recording_id=recording.id).first()
    spectrogram = Spectrogram.query.filter_by(recording_id=recording.id).first()
    pianoroll = Pianoroll.query.filter_by(recording_id=recording.id).first()
    print(recording)
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
        filepath = f'./user_uploads/{user.username}/{filename}'
        file.save(filepath)
        record.txtFileName = filename
        db.session.commit()
    # else:
    #     filepath = record.ground_truth
    #
    # lines = []
    #
    # if filepath:
    #     f = open(filepath, 'r')
    #     for line in f:
    #         lines.append(line.strip())
    return jsonify('File Uploaded')


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


        recording = Recording(filename=record_name_trimmed,
                              filepath=filepath,
                              user=user,
                              isTrackSelected=True,
                              isWaveform=True,
                              isWaveformDisplayed=True,
                              splitChannels=False,
                              waveformColor=record.waveformColor,
                              backgroundColor=record.backgroundColor
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
@app.route('/get-spectrogram/<record_name>', methods=['POST', 'GET'])
@jwt_required()
def createSpectrogram(record_name):
    user = current_user
    filepath = os.path.realpath(f'./user_uploads/{user.username}/{record_name}')

    y, sr = librosa.load(filepath)

    print(y)
    # N = 2048
    # H = 2036
    # Y_stft = librosa.stft(x)
    # # S_db = np.abs(Y_stft) ** 2
    # # D = librosa.stft(x)
    # S_db_hr = librosa.amplitude_to_db(np.abs(Y_stft), ref=np.max)
    #
    # # plt.figure(figsize=(60, 4))
    # # librosa.display.specshow(S_db_hr, hop_length=256, x_axis='time', y_axis='log')
    # # plt.colorbar()
    # # plt.show()
    # return jsonify(S_db_hr.tolist())
@app.route('/spectrogram/<record_name>', methods=['POST', 'GET'])
@jwt_required()
def spectrogram(record_name):
    user = current_user
    filepath = os.path.realpath(f'./user_uploads/{user.username}/{record_name}')

    x, sr = librosa.load(filepath, duration=5)

    # M = librosa.feature.melspectrogram(y=x, sr=sr, n_fft=1024)
    # M_db = librosa.power_to_db(M, ref=np.max)


    Y_stft = librosa.stft(x,n_fft=512)
    S_db_hr = librosa.power_to_db(np.abs(Y_stft), ref=np.max)
    librosa.display.specshow(S_db_hr, y_axis='log', x_axis='time')
    plt.colorbar()
    plt.show()
    librosa.display.specshow(S_db_hr, y_axis='linear', x_axis='time')
    plt.colorbar()
    plt.show()
    return jsonify(S_db_hr.tolist())
