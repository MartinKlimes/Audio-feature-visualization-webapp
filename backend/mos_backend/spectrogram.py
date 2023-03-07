import numpy as np
import matplotlib.pyplot as plt
import os
import librosa
import librosa.display
from flask import jsonify
import time
def f_pitch(p, pitch_ref=69, freq_ref=440.0):
    return 2 ** ((p - pitch_ref) / 12) * freq_ref


def pool_pitch(p, Fs, N, pitch_ref=69, freq_ref=440.0):
    lower = f_pitch(p - 0.5, pitch_ref, freq_ref)
    upper = f_pitch(p + 0.5, pitch_ref, freq_ref)
    k = np.arange(N // 2 + 1)
    k_freq = k * Fs / N  # F_coef(k, Fs, N)
    mask = np.logical_and(lower <= k_freq, k_freq < upper)

    return k[mask]
def createSpectrogram():



    x, sr = librosa.load('Gel.mp3')

    Y_stft = librosa.stft(x, n_fft=256)

    S_db_hr = librosa.amplitude_to_db(np.abs(Y_stft), ref=np.max)
    print(S_db_hr[0])
    with open("file.txt", "w") as f:
        for s in S_db_hr[4]:
            f.write(str(s) + ",\n")
    librosa.display.specshow(S_db_hr, y_axis='linear', x_axis='time')
    plt.show()
    # plt.figure(figsize=(20, 4))
    # plt.specgram(x[0:1000000], NFFT=2048, Fs=Fs, noverlap=10, cmap='jet_r')
    #
    # plt.show()
    # filepath = os.path.realpath(f'./user_uploads/admin2/chopin_01.mp3')
    #
    # # x, Fs = librosa.load('9904__snoman__grass1.wav')
    #
    # x, Fs = librosa.load('9904__snoman__grass1.wav')
    # # fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
    # # D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    # # img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
    # #                                sr=sr, ax=ax[0])
    # # ax[0].set(title='Linear-frequency power spectrogram')
    # # ax[0].label_outer()
    # # plt.show()
    # N = 2048
    # H = 256
    # Y_stft = librosa.stft(x, hop_length=H, n_fft=N)
    # Y = np.abs(Y_stft) ** 2

    # D = librosa.stft(x)
    # S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    # print(S_db.shape)
    # print(S_db)
    # # fig = plt.figure(figsize=(10, 4))
    #
    # plt.figure(figsize=(20, 4))
    # librosa.display.specshow(S_db)
    # plt.colorbar()
    # plt.show()
    # Y.tolist()
    #
    # with open("file.txt", "w") as f:
    #     for s in jsonify(Y.tolist()):
    #         f.write(str(s) + "\n")
    # Y_LF = np.zeros((128, Y.shape[1]))
    # arr = np.zeros(5)
    # # print(Y[238])
    # # print(Y[238, :].sum(axis=0))
    # for p in range(100,101):
    #     k = pool_pitch(p, Fs, N)
    #
    #     # print(Y.shape)
    #     # print(k)
    #     print(Y[k, :])
    #     # print('ahoj')
    #     print(Y[k, :].sum(axis=0))
    #
    #     Y_LF[p,  :] = Y[k, :].sum(axis=0)


    # F_coef_pitch = np.arange(128)
    #
    # fig = plt.figure(figsize=(10, 4))
    # eps = np.finfo(float).eps
    # plt.imshow(10 * np.log10(eps + Y_LF), origin='lower', aspect='auto', cmap='gray_r',
    #     )
    # plt.clim([-10, 50])
    # plt.ylim([21, 108])
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Frequency (pitch)')
    # cbar = plt.colorbar()
    # cbar.set_label('Magnitude (dB)')
    #
    # plt.tight_layout()
    # plt.show()
    # hop_length = 1024
    # 
    # fig, ax = plt.subplots()
    # fig.set_figwidth(400)
    # # plt.axis('off')
    # 
    # D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)),
    #                             ref=np.max)
    # print(D)
    # plt.figure(figsize=(10, 4))
    # img = librosa.display.specshow(Y_LF, y_axis='log', sr=Fs, hop_length=H,
    #                          x_axis='time')
    # plt.show()
    # # ax.set(title='Log-frequency power spectrogram')
    # # ax.label_outer()
    # fig.colorbar(img, ax=ax, format="%+2.f dB")
    # 
    # plt.savefig('spectrogram',
    #                 pad_inches=0)
    # 
    # fig, ax = plt.subplots()
    # plt.colorbar(img, ax=ax)
    # # ax.remove()
    # plt.savefig('plot_onlycbar_tight.png',bbox_inches='tight',  transparent=True)

    # fig, ax = plt.subplots()
    # plt.colorbar(img, ax=ax)
    # ax.remove()
    # plt.savefig('plot_onlycbar_tight.png', bbox_inches='tight', transparent=True)

    # x, Fs = librosa.load('9904__snoman__grass1.wav')

    # y, sr = librosa.load('chopin2.mp3')
    # D = librosa.stft(y,hop_length=256, n_fft=1024)  # STFT of y
    # S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    # st = time.time()
    #
    # fig, ax = plt.subplots()
    #
    # img = librosa.display.specshow(S_db, x_axis='time', y_axis='linear', ax=ax)
    #
    # fig.colorbar(img, ax=ax, format="%+2.f dB")
    # et = time.time()
    # print(img)
    # plt.savefig('plot_onlycbar_tight.png',bbox_inches='tight',  transparent=True)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # # plt.specgram(y, sr)
    # # plt.title('Spectrogram Using matplotlib.pyplot.specgram() Method')
    # # plt.xlabel("DATA")
    # # plt.ylabel("TIME")
    # # plt.show()
    # elapsed_time = et - st
    # print('Execution time:', elapsed_time, 'seconds')
if __name__ == '__main__':
    createSpectrogram()

