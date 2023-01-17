import numpy as np
import matplotlib.pyplot as plt
import os
import librosa
import librosa.display


def createSpectrogram():
    y, sr = librosa.load('chopin2.mp3')
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

    plt.savefig('spectrogram', bbox_inches='tight',
                    pad_inches=0, transparent=True)

    fig, ax = plt.subplots()
    plt.colorbar(img, ax=ax)
    # ax.remove()
    plt.savefig('plot_onlycbar_tight.png',bbox_inches='tight',  transparent=True)

    # fig, ax = plt.subplots()
    # plt.colorbar(img, ax=ax)
    # ax.remove()
    # plt.savefig('plot_onlycbar_tight.png', bbox_inches='tight', transparent=True)


    # y, sr = librosa.load('chopin.mp3')
    # D = librosa.stft(y)  # STFT of y
    # S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    # plt.figure()
    # librosa.display.specshow(S_db)
    # plt.colorbar()


    # plt.specgram(y, sr)
    # plt.title('Spectrogram Using matplotlib.pyplot.specgram() Method')
    # plt.xlabel("DATA")
    # plt.ylabel("TIME")
    # plt.show()

if __name__ == '__main__':
    createSpectrogram()
