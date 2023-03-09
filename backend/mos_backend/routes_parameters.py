from mos_backend import app, db
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename

import os
import numpy as np
import librosa.display
from flask_jwt_extended import jwt_required, current_user
from flask import request, jsonify, send_from_directory, send_file
import json


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


# @app.route('/get-pianoroll/<start>/<end>/', methods=[ 'GET', 'POST'])
# @jwt_required()
# def get_pianoroll(start, end):
#     user = current_user
#
#
#
#
#     filepath_midi = os.path.realpath(f'./user_uploads/{user.username}/MIDI/data_midi_chopin_01.mid')
#     pm = pretty_midi.PrettyMIDI(filepath_midi)
#
#     def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
#         # Use librosa's specshow function for displaying the piano roll
#         librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch],
#                                  hop_length=1, sr=fs, x_axis='time', y_axis='cqt_note',
#                                  fmin=pretty_midi.note_number_to_hz(start_pitch))
#
#     plt.figure(figsize=(83.83, 3))
#     plt.axis('off')
#
#     # fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
#     plot_piano_roll(pm, 24, 100)
#     if (start != 'undefined') and (end != 'undefined'):
#         if start.isdigit():
#             start = int(start)
#         else:
#             start = float(start)
#         if end.isdigit():
#             end = int(end)
#         else:
#             end = float(end)
#         plt.xlim(start, end);
#
#     filepath_pianoroll = os.path.realpath(f'./user_uploads/{user.username}/MIDI/pianoroll.png')
#     plt.savefig(filepath_pianoroll, bbox_inches='tight',
#                 pad_inches=0)
#     image = os.path.realpath(f'./user_uploads/{user.username}/MIDI/pianoroll.png')
#     return send_file(filepath_pianoroll, mimetype='image/png')
#

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

@app.route('/get-spectrogram', methods=[ 'GET', 'POST'])
@jwt_required()
def get_spectrogram():
    user = current_user
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

    y, sr = librosa.load(os.path.realpath(f'./user_uploads/{user.username}/chopin_01.mp3'))
    hop_length = 1024

    fig, ax = plt.subplots()
    fig.set_figwidth(400)
    # plt.axis('off')

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)),
                                ref=np.max)
    img = librosa.display.specshow(D, y_axis='log', sr=sr, hop_length=hop_length,
                             x_axis='time', ax=ax)
    # ax.set(title='Log-frequency power spectrogram')
    # ax.label_outer()
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    filepath_spectrogram = os.path.realpath(f'./user_uploads/{user.username}/spectrogram.png')
    plt.savefig(filepath_spectrogram, bbox_inches='tight',
                    pad_inches=0, transparent=True)

    return send_file(filepath_spectrogram, mimetype='image/png')