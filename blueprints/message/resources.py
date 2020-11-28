
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
        parser = reqparse.RequestParser()
        parser.add_argument('user2_id', location='args', required=True)
        parser.add_argument('message', location='args')
        args = parser.parse_args()
        
        claims = get_jwt_claims()
        
        if args['user2_id'] == claims['id']:
            app.logger.debug('DEBUG: Cannot send to self')
            return {'status': 'error send message'}, 403
        
        conversation = Conversations.query.filter_by(user1_id=claims['id'])
        conversation = conversation.filter_by(user2_id=args['user2_id']).first()
        
        if conversation is None:
            conversation = Conversations.query.filter_by(user2_id=claims['id'])
            conversation = conversation.filter_by(user1_id=args['user2_id']).first()
        
            if conversation is None:
                conversation = Conversations(claims['id'], args['user2_id'])
                db.session.add(conversation)
                db.session.commit()        
        
        personal_message = PersonalMessages(claims['id'], conversation.id, args['message'])
        db.session.add(personal_message)
        db.session.commit()
        
        app.logger.debug('DEBUG: success')
        return marshal(personal_message, PersonalMessages.response_fields), 200

api.add_resource(MessageResource, '', '/<id>')