from flask import Flask,jsonify,request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager,create_access_token
from backend_api.app.config import config
from utils.log_util import Logger
from utils.pid_util import ProcessIdUtil
import subprocess
import datetime
import sys
import os
import requests

enviroment = "production"

if len(sys.argv) == 2:
    print('python <api.py> <development|staging>')
    enviroment = sys.argv[1]

logger = Logger(logs_directory=config.LOG_PATH['logs'], module_id=1 ,module_name='API', table_name='api_logs')
logger.create_directory()
logger.config_logging()


app =  Flask(__name__)  

CORS(app)
app.config.from_object(config.app_config['development'])
api = Api(app)
db = SQLAlchemy(app)


jwt = JWTManager(app)

blacklist = set()

@app.before_request
def do_before_request():
    bearer_token = request.headers.get("Authorization").replace('Bearer ','')
    auth_address = os.environ.get("USER_AUTH_address")
    auth_port = os.environ.get("USER_AUTH_port")
    auth_url = 'http://{0}:{1}/token/validate'.format(auth_address,auth_port)
    head = {'Authorization': 'Bearer {}'.format(bearer_token)}
    response = requests.post(auth_url, headers=head)
    if (response.status_code == 200):
        pass
    else:
        return {"response": response.status_code, "message":"Unauthorized token"}
   
from backend_api.app.routes import urls
from backend_api.app.config import default_handling
from backend_api.app.config import restart_service