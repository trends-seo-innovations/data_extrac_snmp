import os
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.database_util import DatabaseUtil
import datetime

class Logger():
    def __init__(self, logs_directory=None, module_id=None, module_name=None, table_name=None, use_db=True):
        self.logs_directory = logs_directory
        self.module_name = module_name
        self.table_name = table_name
        self.module_id = module_id
        self.use_db = use_db

        try:
            self.conn = DatabaseUtil(os.environ.get("DB_CONN"), os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), os.environ.get("DB_NAME"))
        except Exception as err:
            print(err)
            exit(0)

    def create_directory(self):
        if not os.path.exists(os.path.join(os.getcwd(), self.logs_directory)):
            os.mkdir(os.path.join(os.getcwd(), self.logs_directory))

    def config_logging(self, use_datetime=False):
        module_name = self.module_name.replace(' ', '_').lower()
        now = datetime.datetime.now()
        if use_datetime:
            module_name = module_name + '_' + now.strftime("%Y%m%d")
        log_handler = TimedRotatingFileHandler(os.path.join(os.getcwd(), self.logs_directory, module_name + '.log'), when='midnight')
        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        log_handler.setFormatter(log_formatter)
        log_handler.suffix = '%Y%m%d'
        self.logger = logging.getLogger('logger')
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logging.INFO)

    def log(self, description, log_type='INFO'):
        log = ""
        if self.use_db:
            log = '{0} ({1}) : {2}'.format(self.module_name, self.module_id, description)
            print(log)
        else:
            log = '{0} : {1}'.format(self.module_name, description)

        log_type = str(log_type).upper()
       
        if log_type == 'CRITICAL':
            self.logger.critical(log)
        elif log_type == 'WARNING':
            self.logger.warning(log)
        elif log_type == 'ERROR':
            self.logger.error(log)
        elif log_type == 'DEBUG':
            self.logger.debug(log)
        else:
            self.logger.info(log)
            
        log = log.replace('\'', '\"')

        if self.use_db:
            query_string = 'INSERT INTO {0} values ({1}, \'{2}\', \'{3}\', DEFAULT)'.format(self.table_name, self.module_id, log_type, log)
            try:
                self.conn.insert_query(query_string)
            except Exception as err:
                log = '{0} ({1}) : {2}'.format(self.module_name, self.module_id, err)
                print(log)
                # exit(0)


