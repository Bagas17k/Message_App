from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Messages(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.Text())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    room_id = db.Column(db.Integer, ForeignKey(Rooms.id, ondelete='CASCADE'), nullable=False)
    
    response_fields = {
        'id' :  fields.Integer,
        'message' : fields.String,
    }

    def __init__(self, message):
        self.message = message
        
    def __repr__(self):
        return '<Message %r>' % self.id