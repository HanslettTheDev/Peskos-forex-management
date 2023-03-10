from datetime import datetime
from peskos import db
from sqlalchemy.sql import false

class VerifiedRecords(db.Model):

    __tablename__ = "verified_records"
    id = db.Column(db.Integer, primary_key=True)
    is_initiated = db.Column(db.Boolean, nullable=False, server_default=false())
    has_payed = db.Column(db.Boolean, nullable=False, server_default=false())
    date_initiated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_verified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)

    def __repr__(self):
        return f"Verified Records ('{self.id}')"