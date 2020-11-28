
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims
import json
from .model import Messages
from blueprints.room.model import Rooms
from blueprints.user.model import Users
from blueprints import db, app
from sqlalchemy import desc

bp_message = Blueprint('message', __name__)
api = Api(bp_message)

class MessageResource(Resource):
    def options(self):
        return {'status':'ok'}, 200
    
    def post(self):
        pass
        
api.add_resource(MessageResource, '', '/<id>')