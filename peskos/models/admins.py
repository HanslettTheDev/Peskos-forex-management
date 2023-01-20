from flask_login import UserMixin
from peskos import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))

class Admins(db.Model, UserMixin):
    
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, default="")
    login_id = db.Column(db.Integer(), nullable=False, default="")
    password = db.Column(db.String(150), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='admin_roles', backref='type', lazy=True, cascade="delete")

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"