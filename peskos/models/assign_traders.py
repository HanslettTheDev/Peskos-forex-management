from peskos import db

class AssignTraders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trading_assistant = db.Column(db.Integer, db.ForeignKey("admins.id"))
    assigned_client = db.Column(db.Integer, db.ForeignKey("clients.id"))