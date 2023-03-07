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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Waveform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isWaveform = db.Column(db.Boolean, nullable=True)
    isWaveformDisplayed = db.Column(db.Boolean, nullable=True)

    waveformColor = db.Column(db.String(128), nullable=True)
    waveformHeight = db.Column(db.Integer, nullable=True)

    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)

    def __repr__(self):
        return f'Waveform for recording {self.recording_id}'

class Spectrogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isSpectrogram = db.Column(db.Boolean, nullable=True)
    isSpectrogramDisplayed = db.Column(db.Boolean, nullable=True)

    spectrogramColormap = db.Column(db.String(128), nullable=True)
    spectrogramHeight = db.Column(db.Integer, nullable=True)

    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)
class Pianoroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isPianoroll = db.Column(db.Boolean, nullable=True)
    isPianorollDisplayed = db.Column(db.Boolean, nullable=True)

    pianorollColor = db.Column(db.String(256), nullable=True)
    pianorollHeight = db.Column(db.Integer, nullable=True)

    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)