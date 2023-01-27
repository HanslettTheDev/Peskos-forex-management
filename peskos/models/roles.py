from peskos import db

#Define the UserRoles association table
class AdminRoles(db.Model):
    __tablename__ = 'admin_roles'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id', ondelete='CASCADE'))
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

# Role Model contains all the different user roles like admin, superadmin, user
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))

    @staticmethod
    def enter_role():
        roles = [Role(role="superadmin"), Role(role="admin")]
        for role in roles:
            db.session.add(role)
            db.session.commit()
