import snmp_util.resources.sql_utils as sql_utils
from utils.database_util import DatabaseUtil
from jinjasql import JinjaSql
import pymssql
import sys
import os
import time


class Pollerutil():
    def __init__(self, poller_id):
        self.poller_id = poller_id
        self.jinja = JinjaSql(param_style='pyformat')

        try:
           self.conn = pymssql.connect(
                server=os.environ.get("DB_CONN"), user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD"), database=os.environ.get("SNMPDB"), login_timeout=30)
        except Exception as err:
            sys.exit()

    def get_poller_info(self):
        try:
            template = sql_utils.sql_templates['poller_config'].value
            data = {'poll_id' : str(self.poller_id)}
            poller_info = self.jinja_select_query(template, data)
            return_data = {}
            if poller_info:
                return poller_info
            else:
                log = 'Poller does not exist. Service not started.'
                
                print(log)
                sys.exit()
        except Exception as err:
            sys.exit()

    def jinja_select_query(self, template= None, data=None):
        resultset = []
        query, bind_params = self.jinja.prepare_query(template, data)
        no_except = True
        while no_except:
            try:
                db_conn = self.conn
                cursor = db_conn.cursor(as_dict=True)
                cursor.execute(query,dict(bind_params))
                resultset = cursor.fetchall()
                no_except = False
                cursor.close()
                return resultset
            except Exception as err:
                db_conn.rollback()
                if self.deadlock_validator(err):         
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                else:
                    raise ValueError("Error encountered while selecting data from the database: %s" % (err))  
            finally:   
                db_conn.close()