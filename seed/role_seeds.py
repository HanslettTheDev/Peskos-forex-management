from flask_seeder import Seeder
from peskos.models.role_model import Role

class RoleSeeder(Seeder):
    def run(self):
        roles = [Role(role="superadmin"), Role(role="admin")]
        for role in roles:
            print(f"Added {role}")
            self.db.session.add(role)