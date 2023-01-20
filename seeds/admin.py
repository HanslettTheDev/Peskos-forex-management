from flask_seeder import Seeder
from peskos import bcrypt
from peskos.models.roles import Role
from peskos.models.admins import Admins


class AdminSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 2

    def run(self):
        password = bcrypt.generate_password_hash("peskosadmin")
        password2 = bcrypt.generate_password_hash("password")
        admin_role = Role.query.filter_by(role="superadmin").first()
        admin_role2 = Role.query.filter_by(role="admin").first()
        
        admin = Admins(first_name="Jack", last_name="Kinyua", 
        username = "@jjkinyua", password=password
        )
        admin2 = Admins(first_name="Jack", last_name="Kinyua", 
        login_id = 1234, password=password2
        )

        admin.roles = [admin_role,]
        admin2.roles = [admin_role2,]

        
        self.db.session.add(admin)
        self.db.session.add(admin2)
        print("Added new superadmin")