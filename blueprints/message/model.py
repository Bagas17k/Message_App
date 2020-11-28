from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from blueprints.room.model import Rooms
from blueprints.user.model import Users

class Messages(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    message = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    room_id = db.Column(db.Integer, ForeignKey(Rooms.id, ondelete='CASCADE'), nullable=False)
    
    response_fields = {
        'id' :  fields.Integer,
        'sender_id' : fields.Integer,
        'message' : fields.String,
        'room_id' : fields.Integer,
    }

    def __init__(self, sender_id, message, room_id):
        self.sender_id = sender_id
        self.message = message
        self.room_id = room_id

    def __repr__(self):
        return '<Message %r>' % self.id