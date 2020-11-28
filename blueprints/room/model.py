from blueprints import db
from flask_restful import fields
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from blueprints.user.model import Users

class Rooms(db.Model):
    __tablename__ = "room"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id_1 = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    user_id_2 = db.Column(db.Integer, ForeignKey(Users.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    message = db.relationship("Messages", cascade="all, delete-orphan", passive_deletes=True)

    response_fields = {
        'id' :  fields.Integer,
        'user_id_1' : fields.Integer,
        'user_id_2' : fields.Integer,
    }

    def __init__(self, user_id_1, user_id_2):
        self.user_id_1 = user_id_1
        self.user_id_2 = user_id_2
        
    def __repr__(self):
        return '<Room %r>' % self.id