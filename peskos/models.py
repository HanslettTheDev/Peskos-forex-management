from datetime import datetime
from peskos import db
# from flask_login import LoginManager, UserMixin


# @LoginManager.user_loader
# def load_user(user_id):
#     return Clients.query.get(user_id)

class SuperAdmins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)

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