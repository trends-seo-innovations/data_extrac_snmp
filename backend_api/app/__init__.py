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

CORS(app,resources={r"/*": {"origins": "*"}})
app.config.from_object(config.app_config['development'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
blacklist = set()



from backend_api.app.routes import urls
from backend_api.app.config import default_handling
from backend_api.app.config import restart_service