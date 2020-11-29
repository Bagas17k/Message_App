from flask import Blueprint
from flask_restful import Api, reqparse, Resource, marshal, inputs
from sqlalchemy import desc
from .model import Users
from datetime import datetime
import werkzeug, hashlib, uuid
from blueprints import db, app
from flask_jwt_extended import get_jwt_claims, jwt_required

bp_user = Blueprint('User', __name__)
api = Api(bp_user)

class UserResource(Resource):
    def options(self):
        return {'status': 'ok'}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nama', location='json', required=True)
        parser.add_argument('nomor_hp', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()
        
        # encoded password using hashlib and uuid
        salt = uuid.uuid4().hex
        encoded = ('%s%s' % (args['password'], salt)).encode('utf-8')
        hash_pass = hashlib.sha512(encoded).hexdigest()

        user = Users(args['nama'], args['nomor_hp'], hash_pass, salt)
        db.session.add(user)
        db.session.commit()

        app.logger.debug('DEBUG : %s', user)

        return marshal(user, Users.response_fields), 200, {'Content-Type': 'application/json'}

api.add_resource(UserResource, '')