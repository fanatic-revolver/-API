from exts import db
from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    submission_time = db.Column(db.DateTime, nullable=False, default=datetime.now)