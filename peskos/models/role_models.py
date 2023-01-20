from peskos import db

#Define the UserRoles association table
# association_table = db.Table("user_roles",
#     db.Column(db.Integer, db.ForeignKey('admins.id', ondelete='CASCADE'), primary_key=True),
#     db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
# )

# Role Model contains all the different user roles like admin, superadmin, user
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), unique=True)
    