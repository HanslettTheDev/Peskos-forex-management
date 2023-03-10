from flask_login import UserMixin
from peskos import db, login_manager, bcrypt
from peskos.models.client import Clients
from peskos.models.roles import AdminRoles, Role
from peskos.models.assign_traders import AssignTraders

@login_manager.user_loader
def load_user(user_id):
    return Admins.query.get(int(user_id))


class Admins(db.Model, UserMixin):
    
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_assigned = db.Column(db.Boolean, nullable=False, default=False)
    roles = db.relationship('Role', secondary='admin_roles', uselist=False, cascade="all")
    client = db.relationship('Clients', backref="author", lazy=True)
    assigned_admin = db.relationship("AssignTraders", backref="admin", lazy=True)

    @staticmethod
    def add():
        password = bcrypt.generate_password_hash("peskosadmin")
        role = Role.query.filter_by(role="super admin").first()
        
        admin = Admins(first_name="Jack", last_name="Kinyua", 
        email="helloworld@gmail.com", password=password)

        admin.roles = role

        db.session.add(admin)
        db.session.commit()
        

    def __repr__(self):
        return f"User('{self.email}', '{self.first_name}')"
