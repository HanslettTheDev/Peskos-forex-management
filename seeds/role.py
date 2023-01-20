from flask_seeder import Seeder

from peskos.models.roles import Role

class RoleSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db=db)
        self.priority = 1

    def run(self):
        roles = [Role(role="superadmin"), Role(role="admin")]
        for role in roles:
            print(f"Added {role}")
            self.db.session.add(role)