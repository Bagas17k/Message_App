import json
import config
import os

from flask_cors import CORS, cross_origin
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_script import Manager
from functools import wraps

app = Flask(__name__)
jwt = JWTManager(app)
app.config['APP_DEBUG'] = True
CORS(app, origins="*", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)


#  Environtment choices
flask_env = os.environ.get('FLASK_ENV', 'Production')
if flask_env == "Production":
    app.config.from_object(config.ProductionConfig)
elif flask_env == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.before_request
def before_request():
    if request.method != 'OPTIONS':  # <-- required
        pass
    else:
        return {}, 200, {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'POST, PATCH, GET, DELETE', 'Access-Control-Allow-Headers': '*'}

# log hadler
@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning("REQUEST_LOG\t%s",
                           json.dumps({
                               'method': request.method,
                               'code': response.status,
                               'uri': request.full_path,
                               'request': requestData,
                               'response': json.loads(response.data.decode('utf-8'))
                           })
                           )
    else:
        app.logger.error("REQUEST_LOG\t%s",
                         json.dumps({
                             'method': request.method,
                             'code': response.status,
                             'uri': request.full_path,
                             'request': requestData,
                             'response': json.loads(response.data.decode('utf-8'))
                         }))
    return response

# import blueprints
from blueprints.jwt.resources import bp_jwt
from blueprints.user.resources import bp_user
from blueprints.message.resources import bp_message

# set blueprints
app.register_blueprint(bp_jwt, url_prefix='/login')
app.register_blueprint(bp_user, url_prefix='/user')
app.register_blueprint(bp_message, url_prefix='/message')


db.create_all()