from peskos import create_app
from peskos.models.admins import Admins
from peskos.models.roles import Role
from peskos import db

app = create_app()

if __name__ == "__main__":
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    #     Role().enter_role()
    #     Admins().add()
    app.run(debug=True)