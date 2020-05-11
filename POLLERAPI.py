from backend_api.app import app
from backend_api.app import logger
from utils.log_util import Logger
from utils.pid_util import ProcessIdUtil
from backend_api.app.config import config
import os


app.run(host='0.0.0.0',port=4044)
