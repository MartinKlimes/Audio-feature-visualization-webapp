from mos_backend import app, db

with app.app_context():
    db.create_all()
