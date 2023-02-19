from datetime import datetime
from peskos import db

class TradingRecords(db.Model):
    
    __tablename__ = "trading_records"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.Integer, nullable=False)
    initial_amount = db.Column(db.Integer, nullable=False)
    final_amount = db.Column(db.Integer, nullable=False)
    profit = db.Column(db.Integer, nullable=False)
    acc_statement = db.Column(db.String(), nullable=False, default="No statement!")
    
    date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Trading records ('{self.name}', '{self.acc_statement}')"