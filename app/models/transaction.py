import enum
from app.extensions import db

class TypeEnum(str, enum.Enum):
    income  = "income"
    expense = "expense"

class Transaction(db.Model):
    __tablename__ = "transactions"
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount     = db.Column(db.Float, nullable=False)
    type       = db.Column(db.Enum(TypeEnum), nullable=False)
    category   = db.Column(db.String(80), nullable=False)
    date       = db.Column(db.Date, nullable=False)
    notes      = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, server_default=db.func.now())