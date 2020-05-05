from backend_api.app import app
from backend_api.app import logger
from utils.log_util import Logger
from utils.pid_util import ProcessIdUtil
from backend_api.app.config import config
import os

# app.run(host='0.0.0.0', port=os.environ.get("API_PORT"), ssl_context=('localhost+2.pem', 'localhost+2-key.pem'))

# pid_util = ProcessIdUtil(config.LOG_PATH['pid'], 1, 'backend_api', 'backend_api', None)
# pid_util.create_directory()

# if pid_util.is_process_running_without_db():
#     logger.log("API is already running..")
# else:
#     pid_util.create_pid()
app.run(host='0.0.0.0',port=os.environ.get("API_PORT"))