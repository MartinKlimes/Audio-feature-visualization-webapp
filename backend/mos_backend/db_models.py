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
    ground_truth = db.Column(db.String(128), unique=True, nullable=False)
    # optional parameters
    year = db.Column(db.Integer, unique=False, nullable=True)
    performer = db.Column(db.String(128), unique=False, nullable=True)
    # a user who uploaded this recording
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

