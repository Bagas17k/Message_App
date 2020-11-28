from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims

import hashlib
import uuid
from blueprints.user.model import Users

bp_jwt = Blueprint('jwt', __name__)
api = Api(bp_jwt)

class CreateTokenResource(Resource):
    
    # create jwt token 
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nomor_hp', location='json', required=True, type=str)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        qry_user = Users.query.filter_by(
        nomor_hp = args['nomor_hp']).first()
      
        if qry_user is not None:
            user_salt = qry_user.salt
            # user_type = qry_user.user_type
            encoded = ('%s%s' % (args['password'], user_salt)).encode('utf-8')
            hash_pass = hashlib.sha512(encoded).hexdigest()
            if hash_pass == qry_user.password and qry_user.nomor_hp == args['nomor_hp']:
                qry_user = marshal(qry_user, Users.jwt_fields)
                qry_user['identifier'] = "message_app"
                token = create_access_token(
                    identity=args['nomor_hp'], user_claims=qry_user)
                return {'token': token}, 200
        
        return {'status': 'UNAUTHORIZED', 'message': 'invalid key or secret'}, 401


api.add_resource(CreateTokenResource, '')