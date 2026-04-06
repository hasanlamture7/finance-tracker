import enum
from app.extensions import db

class RoleEnum(str, enum.Enum):
    viewer  = "viewer"
    analyst = "analyst"
    admin   = "admin"

class User(db.Model):
    __tablename__ = "users"
    id           = db.Column(db.Integer, primary_key=True)
    email        = db.Column(db.String(120), unique=True, nullable=False)
    password     = db.Column(db.String(200), nullable=False)
    role         = db.Column(db.Enum(RoleEnum), default=RoleEnum.viewer)
    created_at   = db.Column(db.DateTime, server_default=db.func.now())
    transactions = db.relationship("Transaction", backref="owner", lazy=True)