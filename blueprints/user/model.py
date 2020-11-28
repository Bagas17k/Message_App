from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy.orm import relationship


class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100), nullable=False)
    nomor_hp = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    sender_id = db.relationship("Rooms", cascade="all, delete-orphan", passive_deletes=True)
    receiver_id = db.relationship("Rooms", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        'id' :  fields.Integer,
        'nama' : fields.String,
        'nomor_hp' : fields.String,
    }

    jwt_fields = {
        'id' :  fields.Integer,
        'nama' : fields.String,
        'nomor_hp' : fields.String,
    }

    def __init__(self, nama, nomor_hp, password, salt):
        self.nama = nama
        self.nomor_hp = nomor_hp
        self.password = password
        self.salt = salt

    def __repr__(self):
        return '<User %r>' % self.id