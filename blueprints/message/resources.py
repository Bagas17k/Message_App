
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from flask_jwt_extended import get_jwt_claims, jwt_required
from datetime import datetime
import json
from .model import Messages
from blueprints.room.model import Rooms
from blueprints.user.model import Users
from blueprints import db, app
from sqlalchemy import desc, or_

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

        # get data for receiver message using phone number
        receiver = Users.query.filter_by(nomor_hp=args['nomor_hp']).first()
        user_id_2 = receiver.id
        
        # condition cannot send message to self
        if user_id_2 == claims['id']:
            app.logger.debug('DEBUG: Cannot send to self')
            return {'status': 'error send message'}, 403
        
        # selecion for room chat
        room = Rooms.query.filter_by(user_id_1=claims['id'])
        room = room.filter_by(user_id_2=user_id_2).first()
        
        # if there is no room chat filter again
        if room is None:
            room = Rooms.query.filter_by(user_id_2=claims['id'])
            room = room.filter_by(user_id_1=user_id_2).first()

            # if there is no room chat make new rom
            if room is None:
                # make a new room chat
                room = Rooms(claims['id'], user_id_2)
                db.session.add(room)
                db.session.commit()        
        
        message = Messages(claims['id'], args['message'], room.id)
        room.updated_at = datetime.now()
        db.session.add(message)
        db.session.commit()
        
        app.logger.debug('DEBUG: success')
        return marshal(message, Messages.response_fields), 200

class RoomResource(Resource):
    
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        list_rooms = []

        # get room data per user login
        rooms = Rooms.query.filter(or_(Rooms.user_id_1.like(claims['id']), Rooms.user_id_2.like(claims['id'])))

        for room in rooms:
            data_room = marshal(room, Rooms.response_fields)

            # get data user that login
            user_login = Users.query.get(claims["id"])
            user_login = marshal(user_login, Users.response_fields)
            data_room["user_login"] = user_login

            # get data of partner chat i room
            if data_room['user_id_1'] != claims["id"]:
                user = Users.query.get(data_room["user_id_1"])
                data_user = marshal(user, Users.response_fields)
                data_room["room_patner"] = data_user
            
            if data_room['user_id_2'] != claims["id"]:
                user = Users.query.get(data_room["user_id_2"])
                data_user = marshal(user, Users.response_fields)
                data_room["room_patner"] = data_user
            
            # get message per room id spcific with room partner
            messages = Messages.query.filter_by(room_id=room.id)

            list_messages = []
            for message in messages:
                data_message = marshal(message, Messages.response_fields)
                
                # get data sender per message
                sender = Users.query.get(message.sender_id)
                data_sender = marshal(sender, Users.response_fields)
                data_message["sender"] = data_sender
                list_messages.append(data_message)

            data_room["all_messages"] = list_messages
            list_rooms.append(data_room)

        return list_rooms, 200
        


api.add_resource(MessageResource, '', '/<id>')
api.add_resource(RoomResource, '/room', '')