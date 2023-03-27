from mos_backend import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    recordings = db.relationship('Recording', backref='user')

    # how the object is printed in the console
    def __repr__(self):
        return f'User: ({self.username}, {self.email})'


class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), unique=False, nullable=False)
    filepath = db.Column(db.String(128), unique=True, nullable=False)
    ground_truth = db.Column(db.String(128), unique=True, nullable=True)
    isTrackSelected = db.Column(db.Boolean, unique=False, nullable=True)


    backgroundColor = db.Column(db.String(128), nullable=True)
    txtFileName = db.Column(db.String(128), nullable=True)
    MIDIFileName = db.Column(db.String(128), nullable=True)
    splitChannels = db.Column(db.Boolean, nullable=True)
    # optional parameters
    # year = db.Column(db.Integer, unique=False, nullable=True)
    # performer = db.Column(db.String(128), unique=False, nullable=True)
    # a user who uploaded this recording
    waveform = db.relationship('Waveform', backref='recording', uselist=False)
    pianoroll = db.relationship('Pianoroll', backref='recording', uselist=False)
    spectrogram = db.relationship('Spectrogram', backref='recording', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, filename, filepath, user_id, ground_truth=None, isTrackSelected=False, backgroundColor=None,
                 txtFileName=None, MIDIFileName=None, splitChannels=None):
        self.filename = filename
        self.filepath = filepath
        self.ground_truth = ground_truth
        self.isTrackSelected = isTrackSelected
        self.backgroundColor = backgroundColor
        self.txtFileName = txtFileName
        self.MIDIFileName = MIDIFileName
        self.splitChannels = splitChannels
        self.waveform = Waveform(isWaveform=False, isWaveformDisplayed=False, waveformColor="", recording_id=self.id)
        self.spectrogram = Spectrogram(isSpectrogram=False, isSpectrogramDisplayed=False, spectrogramColormap="jet",
                                       spectrogramHeight=256, recording_id=self.id)
        self.pianoroll = Pianoroll(isPianoroll=False, isPianorollDisplayed=False, pianorollColor=None,
                                   pianorollHeight=300, recording_id=self.id)
        self.user_id = user_id
    def to_dict(self):
        return {
            'id': self.id,
            'trackName': self.filename,
            'filepath': self.filepath,
            'ground_truth': self.ground_truth,
            'isTrackSelected': self.isTrackSelected,
            'backgroundColor': self.backgroundColor,
            'txtFileName': self.txtFileName,
            'MIDIFileName': self.MIDIFileName,
            'splitChannels': self.splitChannels,
            'waveform': self.waveform.to_dict() if self.waveform else None,
            'pianoroll': self.pianoroll.to_dict() if self.pianoroll else None,
            'spectrogram': self.spectrogram.to_dict() if self.spectrogram else None
        }

class Waveform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isWaveform = db.Column(db.Boolean, nullable=True)
    isWaveformDisplayed = db.Column(db.Boolean, nullable=True)

    waveformColor = db.Column(db.String(128), nullable=True)
    waveformHeight = db.Column(db.Integer, nullable=True)

    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'isWaveform': self.isWaveform,
            'isWaveformDisplayed': self.isWaveformDisplayed,
            'waveformColor': self.waveformColor,
            'waveformHeight': self.waveformHeight
        }
    def __repr__(self):
        return f'Waveform for recording {self.recording_id}'

class Spectrogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isSpectrogram = db.Column(db.Boolean, nullable=True)
    isSpectrogramDisplayed = db.Column(db.Boolean, nullable=True)

    spectrogramColormap = db.Column(db.String(128), nullable=True)
    spectrogramHeight = db.Column(db.Integer, nullable=True)

    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'isSpectrogram': self.isSpectrogram,
            'isSpectrogramDisplayed': self.isSpectrogramDisplayed,
            'spectrogramColormap': self.spectrogramColormap,
            'spectrogramHeight': self.spectrogramHeight
        }
class Pianoroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isPianoroll = db.Column(db.Boolean, nullable=True)
    isPianorollDisplayed = db.Column(db.Boolean, nullable=True)

    pianorollColor = db.Column(db.String(256), nullable=True)
    pianorollHeight = db.Column(db.Integer, nullable=True)

    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'isPianoroll': self.isPianoroll,
            'isPianorollDisplayed': self.isPianorollDisplayed,
            'pianorollColor': self.pianorollColor,
            'pianorollHeight': self.pianorollHeight
        }