
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims, jwt_required
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
    
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nomor_hp', location='json', required=True)
        parser.add_argument('message', location='json')
        args = parser.parse_args()
        
        claims = get_jwt_claims()

        receiver = Users.query.filter_by(nomor_hp=args['nomor_hp']).first()
        user_id_2 = receiver.id
        
        if user_id_2 == claims['id']:
            app.logger.debug('DEBUG: Cannot send to self')
            return {'status': 'error send message'}, 403
        
        room = Rooms.query.filter_by(user_id_1=claims['id'])
        room = room.filter_by(user_id_2=user_id_2).first()
        
        if room is None:
            room = Rooms.query.filter_by(user_id_2=claims['id'])
            room = room.filter_by(user_id_1=user_id_2).first()
        
            if room is None:
                room = Rooms(claims['id'], user_id_2)
                db.session.add(room)
                db.session.commit()        
        
        message = Messages(claims['id'], args['message'], room.id)
        db.session.add(message)
        db.session.commit()
        
        app.logger.debug('DEBUG: success')
        return marshal(message, Messages.response_fields), 200

api.add_resource(MessageResource, '', '/<id>')