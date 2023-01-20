from datetime import datetime
from peskos import db

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    broker = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    second_number = db.Column(db.Integer, default=0)
    icd = db.Column(db.Integer, nullable=False)
    idcard_number = db.Column(db.String(50), unique=True, nullable=False)
    account_number = db.Column(db.Integer, nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Clients('{self.name}', '{self.email}')"
        