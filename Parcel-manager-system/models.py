from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, func

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parcel_name = db.Column(db.String(150), nullable=False)
    sender = db.Column(db.String(150), nullable=False)
    recipient = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    estimated_date = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, default=func.now())   

    def __repr__(self):
        return f"Parcel('{self.sender}', '{self.recipient}', '{self.status}')"