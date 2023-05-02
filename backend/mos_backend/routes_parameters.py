from mos_backend import app, db
from werkzeug.utils import secure_filename
import os
import librosa

from flask_jwt_extended import jwt_required, current_user
from flask import request, jsonify
import json

@app.route('/get-event-detection/<record_name>')
@jwt_required()
def get_event_detection(record_name):
    user = current_user
    # json_path = f"./user_uploads/{user.username}/{record_name}.json"
    # if os.path.exists(json_path):
    #     with open(json_path, 'r') as f:
    #         data = json.load(f)
    # else:
    #     if ' - trimmed (' in record_name or ' - bars (' in record_name:
    #         y, sr = librosa.load(f'./user_uploads/{user.username}/trimmed_tracks/{record_name}')
    #     else:
    #         y, sr = librosa.load(f'./user_uploads/{user.username}/{record_name}')
    #
    #     onset = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    #     tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    #     data = {'onset': onset.tolist(), 'beats': beats.tolist()}
    #     with open(json_path, 'w') as f:
    #         json.dump(data, f)
    #
    # if 'data_type' in request.args:
    #     data_type = request.args['data_type']
    # else:
    #     data_type = 'onset'
    #
    # if data_type == 'beats':
    #     data = {'beats': data['beats']}
    # else:
    #     data = {'onset': data['onset']}
    # y, sr = librosa.load(f'./user_uploads/{user.username}/{record_name}')
    # print(sr)
    # return jsonify(data)
    # sfo = soundfile.SoundFile(f'./user_uploads/{user.username}/{record_name}')
    y, sr = librosa.load(f'./user_uploads/{user.username}/{record_name}')

    return jsonify(sr)


@app.route('/get-tempo/<filename>/<int:num_segments>')
@jwt_required()
def get_tempo(filename, num_segments):
    user = current_user
    # get audio file from request
    filepath = f'./user_uploads/{user.username}/{filename}'

    # load audio data using librosa
    audio_data, sample_rate = librosa.load(filepath)

    # get number of segments from request
    segment_length = len(audio_data) // num_segments
    # calculate tempo for each segment
    tempos = []
    for i in range(num_segments):
        segment_start = i * segment_length
        segment_end = (i + 1) * segment_length
        segment = audio_data[segment_start:segment_end]
        tempo = librosa.beat.tempo(y=segment, sr=sample_rate)[0]
        tempos.append(tempo)

    # return tempos as JSON response
    return jsonify(tempos)