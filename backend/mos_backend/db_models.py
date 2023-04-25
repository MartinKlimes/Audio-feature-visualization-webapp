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
    isTrackSelected = db.Column(db.Boolean, unique=False, nullable=True)


    backgroundColor = db.Column(db.String(128), nullable=True)
    txtFileName = db.Column(db.String(128), nullable=True)
    MIDIFileName = db.Column(db.String(128), nullable=True)
    start = db.Column(db.Float, nullable=True)
    end = db.Column(db.Float, nullable=True)

    # optional parameters
    # year = db.Column(db.Integer, unique=False, nullable=True)
    # performer = db.Column(db.String(128), unique=False, nullable=True)
    # a user who uploaded this recording
    waveform = db.relationship('Waveform', backref='recording', uselist=False)
    pianoroll = db.relationship('Pianoroll', backref='recording', uselist=False)
    spectrogram = db.relationship('Spectrogram', backref='recording', uselist=False)
    ioi_data = db.relationship('InterOnsetInterval', backref='recording', uselist=False)
    ibi_data = db.relationship('InterBeatInterval', backref='recording', uselist=False)
    imi_data = db.relationship('InterMeasureInterval', backref='recording', uselist=False)
    RMS_data = db.relationship('RMS', backref='recording', uselist=False)
    Tempo_data = db.relationship('Tempo', backref='recording', uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, filename, filepath, user_id, isTrackSelected=False, backgroundColor=None,
                 txtFileName=None, MIDIFileName=None, waveformColor=None, start=None, end=None):
        self.filename = filename
        self.filepath = filepath
        self.isTrackSelected = isTrackSelected
        self.backgroundColor = backgroundColor
        self.txtFileName = txtFileName
        self.MIDIFileName = MIDIFileName
        self.start = start
        self.end = end
        self.waveform = Waveform(isWaveform=False, isWaveformDisplayed=False, waveformColor=waveformColor, waveformHeight=200, splitChannels=False, recording_id=self.id)
        self.spectrogram = Spectrogram(isSpectrogram=False, isSpectrogramDisplayed=False, spectrogramColormap="Jet",
                                       spectrogramHeight=300,fftSamples=1024, windowFunc='hann', recording_id=self.id)
        self.pianoroll = Pianoroll(isPianoroll=False, isPianorollDisplayed=False, pianorollColor=None,
                                   pianorollHeight=300,dynamicNames=False, ActiveNotesColor='red', recording_id=self.id)
        self.ioi_data = InterOnsetInterval(isIOI=False, isIOIDisplayed=False, graph_type="bar",ioi_dataHeight=100, graph_color="rgba(0, 0, 255, 0.5)", recording_id=self.id)
        self.ibi_data = InterBeatInterval(isIBI=False, isIBIDisplayed=False, graph_type="bar", ibi_dataHeight=100, graph_color="rgba(0, 0, 255, 0.5)", recording_id=self.id)
        self.imi_data = InterMeasureInterval(isIMI=False, isIMIDisplayed=False, graph_type="bar", imi_dataHeight=100, graph_color="rgba(0, 0, 255, 0.5)", recording_id=self.id)
        self.RMS_data = RMS(isRMS=False,numOfFrames =100, isRMSDisplayed=False, graph_type="line", RMS_dataHeight=100, graph_color="rgba(0, 0, 255, 0.5)", recording_id=self.id)
        self.Tempo_data = Tempo(isTempo=False,numOfFrames =100, isTempoDisplayed=False, graph_type="line", Tempo_dataHeight=100, graph_color="rgba(0, 0, 255, 0.5)", recording_id=self.id)
        self.user_id = user_id
    def to_dict(self):
        return {
            'id': self.id,
            'trackName': self.filename,
            'filepath': self.filepath,
            'isTrackSelected': self.isTrackSelected,
            'backgroundColor': self.backgroundColor,
            'txtFileName': self.txtFileName,
            'MIDIFileName': self.MIDIFileName,
            'start': self.start,
            'end': self.end,
            'waveform': self.waveform.to_dict() if self.waveform else None,
            'pianoroll': self.pianoroll.to_dict() if self.pianoroll else None,
            'spectrogram': self.spectrogram.to_dict() if self.spectrogram else None,
            'ioi_data': self.ioi_data.to_dict() if self.ioi_data else None,
            'ibi_data': self.ibi_data.to_dict() if self.ibi_data else None,
            'imi_data': self.imi_data.to_dict() if self.imi_data else None,
            'RMS_data': self.RMS_data.to_dict() if self.RMS_data else None,
            'Tempo_data': self.Tempo_data.to_dict() if self.Tempo_data else None,

        }

class Waveform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isWaveform = db.Column(db.Boolean, nullable=True)
    isWaveformDisplayed = db.Column(db.Boolean, nullable=True)

    waveformColor = db.Column(db.String(128), nullable=True)
    waveformHeight = db.Column(db.Integer, nullable=True)
    splitChannels = db.Column(db.Boolean, nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'isWaveform': self.isWaveform,
            'isWaveformDisplayed': self.isWaveformDisplayed,
            'waveformColor': self.waveformColor,
            'waveformHeight': self.waveformHeight,
            'splitChannels': self.splitChannels,

        }
    def __repr__(self):
        return f'Waveform for recording {self.recording_id}'

class Spectrogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isSpectrogram = db.Column(db.Boolean, nullable=True)
    isSpectrogramDisplayed = db.Column(db.Boolean, nullable=True)

    spectrogramColormap = db.Column(db.String(128), nullable=True)
    spectrogramHeight = db.Column(db.Integer, nullable=True)
    fftSamples = db.Column(db.Integer, nullable=True)
    windowFunc = db.Column(db.String(128), nullable=True)

    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'isSpectrogram': self.isSpectrogram,
            'isSpectrogramDisplayed': self.isSpectrogramDisplayed,
            'spectrogramColormap': self.spectrogramColormap,
            'spectrogramHeight': self.spectrogramHeight,
            'fftSamples': self.fftSamples,
            'windowFunc': self.windowFunc
        }
class Pianoroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isPianoroll = db.Column(db.Boolean, nullable=True)
    isPianorollDisplayed = db.Column(db.Boolean, nullable=True)

    pianorollColor = db.Column(db.String(256), nullable=True)
    pianorollHeight = db.Column(db.Integer, nullable=True)
    dynamicNames = db.Column(db.Boolean, nullable=True)
    ActiveNotesColor = db.Column(db.String(256), nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'isPianoroll': self.isPianoroll,
            'isPianorollDisplayed': self.isPianorollDisplayed,
            'pianorollColor': self.pianorollColor,
            'pianorollHeight': self.pianorollHeight,
            'dynamicNames': self.dynamicNames,
            'ActiveNotesColor': self.ActiveNotesColor,
        }
class InterOnsetInterval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    graph_type = db.Column(db.String(256), nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)
    graph_color = db.Column(db.String(256), nullable=True)
    isIOI = db.Column(db.Boolean, nullable=True)
    isIOIDisplayed = db.Column(db.Boolean, nullable=True)
    ioi_dataHeight = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'graph_type': self.graph_type,
            'graph_color': self.graph_color,
            'isIOI': self.isIOI,
            'isIOIDisplayed': self.isIOIDisplayed,
            'ioi_dataHeight': self.ioi_dataHeight
        }

class InterBeatInterval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    graph_type = db.Column(db.String(256), nullable=True)
    graph_color = db.Column(db.String(256), nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)
    isIBI = db.Column(db.Boolean, nullable=True)
    isIBIDisplayed = db.Column(db.Boolean, nullable=True)
    ibi_dataHeight = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'graph_type': self.graph_type,
            'graph_color': self.graph_color,
            'isIBI': self.isIBI,
            'isIBIDisplayed': self.isIBIDisplayed,
            'ibi_dataHeight': self.ibi_dataHeight
        }
class InterMeasureInterval(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    graph_type = db.Column(db.String(256), nullable=True)
    graph_color = db.Column(db.String(256), nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)
    isIMI = db.Column(db.Boolean, nullable=True)
    isIMIDisplayed = db.Column(db.Boolean, nullable=True)
    imi_dataHeight = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'graph_type': self.graph_type,
            'graph_color': self.graph_color,
            'isIMI': self.isIMI,
            'isIMIDisplayed': self.isIMIDisplayed,
            'imi_dataHeight': self.imi_dataHeight
        }
class RMS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numOfFrames = db.Column(db.Integer, nullable=True)
    graph_type = db.Column(db.String(256), nullable=True)
    graph_color = db.Column(db.String(256), nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)
    isRMS = db.Column(db.Boolean, nullable=True)
    isRMSDisplayed = db.Column(db.Boolean, nullable=True)
    RMS_dataHeight = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'numOfFrames': self.numOfFrames,
            'graph_type': self.graph_type,
            'graph_color': self.graph_color,
            'isRMS': self.isRMS,
            'isRMSDisplayed': self.isRMSDisplayed,
            'RMS_dataHeight': self.RMS_dataHeight
        }
class Tempo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numOfFrames = db.Column(db.Integer, nullable=True)
    graph_type = db.Column(db.String(256), nullable=True)
    graph_color = db.Column(db.String(256), nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey('recording.id'), nullable=False)
    isTempo = db.Column(db.Boolean, nullable=True)
    isTempoDisplayed = db.Column(db.Boolean, nullable=True)
    Tempo_dataHeight = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'numOfFrames': self.numOfFrames,
            'graph_type': self.graph_type,
            'graph_color': self.graph_color,
            'isTempo': self.isTempo,
            'isTempoDisplayed': self.isTempoDisplayed,
            'Tempo_dataHeight': self.Tempo_dataHeight
        }