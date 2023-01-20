from peskos import db

#Define the UserRoles association table
association_table = db.Table("user_roles", 
    db.Column("id", db.Integer, primary_key=True),
    db.Column("admin_id", db.Integer, db.ForeignKey('admins.id', ondelete='CASCADE')),
    db.Column("roles_id", db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))
)

# Role Model contains all the different user roles like admin, superadmin, user
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), unique=True)
    