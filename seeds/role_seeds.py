from flask_seeder import Seeder
from peskos.models.roles import Role

class RoleSeeder(Seeder):
    def __init__(self, db=None):
        super().__init__(db)
        self.priority = 10

    def run(self):
        roles = [Role(role="super"), Role(role="admin"), Role(role="trading assistant")]
        for role in roles:
            print(f"Added {role}")
            self.db.session.add(role)