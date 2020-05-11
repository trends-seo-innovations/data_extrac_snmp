import os
import datetime

class Config(object):
    BUNDLE_ERRORS = True
    JWT_HEADER_NAME = 'Authorization'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES =  datetime.timedelta(days=1, seconds=0)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7, seconds=0)
    JWT_ERROR_MESSAGE_KEY = 'message'
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 0
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

class DevelopmentConfig(Config):
    JWT_SECRET_KEY = 'development-key'
    SERVER_HOST = os.environ.get('API_HOST')
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:p@ssw0rd@192.168.73.51:1433/source_extractor_engine?driver=FreeTDS&port=1433&odbc_options='TDS_Version=8.0'"
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://{0}:{1}@{2}:{4}/{3}?driver=FreeTDS&port={4}&odbc_options='TDS_Version=8.0'".format(
    #         os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), 
    #         os.environ.get("DB_CONN"), os.environ.get("DB_NAME"), os.environ.get("DB_PORT"))
   

class StagingConfig(Config):
    JWT_SECRET_KEY = os.urandom(24)
    SERVER_HOST = os.environ.get('API_HOST')
    DEBUG = True
    ENV = 'staging'
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://{0}:{1}@{2}:{4}/{3}?driver=SQL+Server'.format(
            os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), 
            os.environ.get("DB_CONN"), os.environ.get("DB_NAME"), os.environ.get("DB_PORT"))

class ProductionConfig(Config):
    JWT_SECRET_KEY = os.urandom(24)
    SERVER_HOST = os.environ.get('API_HOST')
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://{0}:{1}@{2}:{4}/{3}?driver=SQL+Server'.format(
            os.environ.get("DB_USER"), os.environ.get("DB_PASSWORD"), 
            os.environ.get("DB_CONN"), os.environ.get("DB_NAME"), os.environ.get("DB_PORT"))

class TestingConfig(Config):
    JWT_SECRET_KEY = 'testing-key'
    DEBUG = True
    SERVER_NAME = 'localhost'
    SQLALCHEMY_DATABASE_URI = ''

app_config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

LOG_PATH = {
    'logs': 'api_logs',
    'pid': 'api_pid'
}