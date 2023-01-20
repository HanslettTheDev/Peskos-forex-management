from flask_seeder import Seeder
from peskos import bcrypt
from peskos.models.admin_models import Admins
from peskos.models.role_model import Role

class AdminSeeder(Seeder):
    def run(self):
        password = bcrypt.generate_password_hash("peskosadmin")
        admin_role = Role.query.filter_by(role="superadmin").first()
        admin = Admins(first_name="Jack", last_name="Kinyua", 
        username = "@jjkinyua", password=password
        )

        admin.roles = [admin_role,]
        
        self.db.session.add(admin)
        print("Added new superadmin")