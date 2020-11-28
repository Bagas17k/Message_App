from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Rooms(db.Model):
    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    message = db.relationship("Messages", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        'id' :  fields.Integer,
        'sender_id' : fields.Integer,
        'receiver_id' : fields.Integer,
    }

    def __init__(self, sender_id, receiver_id):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        
    def __repr__(self):
        return '<Room %r>' % self.id