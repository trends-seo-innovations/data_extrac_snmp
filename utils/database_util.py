import pymssql
import os
import sys
from jinjasql import JinjaSql
import time
class DatabaseUtil():
    def __init__(self, server=None, user=None, password=None, database=None, logger=None):
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.logger =  logger
        self.jinja = JinjaSql(param_style='pyformat') 

    def deadlock_validator(self,error_string):
        error_string = str(error_string).split(' ')
        if 'deadlock' in error_string:
            return True
        else:
            return False
        # is_deadlock =  all(elem in error_string for elem in ['deadlocked','deadlock','(1205'])
        # if is_deadlock:
        #     print("Deadlock Encountered. Retrying")
        # return is_deadlock

    def db_logs(self, message="", status='INFO'):
        if self.logger is None:
            pass
        else:
            self.logger.log(message, status)
        


    def get_connection(self, api=None ,interval  = 2):
        # try:
        #     conn = pymssql.connect(
        #         server=self.server, user=self.user,
        #         password=self.password, database=self.database, login_timeout=30)
        # except pymssql.DatabaseError as err:
        #     raise pymssql.DatabaseError("Cannot connect to database: %s" % (err))
        # except Exception as err:
        #     raise ValueError("Error in connecting to database: %s" % (err))
        # return conn
        
        no_except = True
        while no_except:
            try:
                conn = pymssql.connect(
                server=self.server, user=self.user,
                password=self.password, database=self.database, login_timeout=30)  
                no_except = False
                # self.db_logs("Connected to database")
                # self.db_logs(no_except)
                return conn      
            except Exception as err:
                
                if api:
                    self.db_logs("Error in connecting to database: {0}".format(err), status="CRITICAL")
                    raise ValueError("Error in connecting to database: %s" % (err))
                else:
                    self.db_logs("Database error :{0}".format(err), status="CRITICAL")
                    print("Database error :{0}".format(err))
                    time.sleep(interval)
                    
                

    def select_query(self, query_string=None, api=False):
        resultset = []
        no_except = True
        while no_except:
            try:
                db_conn = self.get_connection()
                cursor = db_conn.cursor(as_dict=True)
                cursor.execute(query_string)
                resultset = cursor.fetchall()
                no_except = False
                cursor.close()

                return resultset
            except Exception as err:
                db_conn.rollback()
                if self.deadlock_validator(err):
                    self.db_logs("Encountered a deadlock on select query", status='CRITICAL')
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                    self.db_logs("Sleeping for 3 seconds...", status='WARNING')
                else:
                    print()
                    if api:
                        raise ValueError(str(list(err.args)[1].decode("utf-8")).split(".", 10)[0])
                    else:
                        self.db_logs("Error encountered while retrieving data from database: %s" % (str(err)), status='CRITICAL')
                        raise ValueError("Error encountered while retrieving data from database: %s" % (str(err)))        
       
            finally:
                db_conn.close()

    def insert_query(self, query_string=None):
        
        no_except = True
        while no_except:
            try:
                db_conn = self.get_connection()
                cursor = db_conn.cursor()
                cursor.execute(query_string)
                no_except = False       
                db_conn.commit()  
                cursor.close()       
            except Exception as err:
                db_conn.rollback()
                if self.deadlock_validator(err):
                    self.db_logs("Encountered a deadlock on insert query", status='CRITICAL')
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                    self.db_logs("Sleeping for 3 seconds...", status='WARNING')
                else:
                    self.db_logs("Error encountered while adding data to the database: %s" % (str(err)), status='CRITICAL')
                    raise ValueError("Error encountered while adding data to the database: %s" % (err))
            finally:
                db_conn.close()

    def insert_many_query(self, query_string=None, data_many = None):
        
        no_except = True
        while no_except:
            try:
                db_conn = self.get_connection()
                cursor = db_conn.cursor()
                cursor.executemany(query_string,data_many)
                no_except = False 
                db_conn.commit()
                cursor.close()
                self.db_logs("Inserted data...")
            except Exception as err:
                if self.deadlock_validator(err):
                    self.db_logs("Encountered a deadlock on insert many query", status='CRITICAL')
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                    self.db_logs("Sleeping for 3 seconds...", status='WARNING')
                else:
                    db_conn.rollback()
                    self.db_logs("Error encountered while adding data to the database: %s" % (str(err)), status='CRITICAL')
                    raise ValueError("Error encountered while adding data to the database: %s" % (err))  
            finally:
                db_conn.close()
    def test_insert_many_query(self, query_string=None):
        no_except = True
        while no_except:
            try:
                db_conn = self.get_connection()
                cursor = db_conn.cursor()
                cursor.executemany(query_string)
                no_except = False 
                db_conn.commit()   
                cursor.close()      
                      
            except Exception as err:
                if self.deadlock_validator(err):         
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                else:
                    db_conn.rollback()
                    raise ValueError("Error encountered while adding data to the database: %s" % (err))  
            finally:
                db_conn.close()

    def update_query(self, query_string=None):
        no_except = True    
        while no_except:
            try:
                db_conn = self.get_connection()
                cursor = db_conn.cursor()
                cursor.execute(query_string)
                db_conn.commit()   
                cursor.close()          
                no_except = False
            except Exception as err:
                db_conn.rollback()
                if self.deadlock_validator(err):
                    self.db_logs("Encountered a deadlock on update query", status='CRITICAL')
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                    self.db_logs("Sleeping for 3 seconds...", status='WARNING')
                else:
                    self.db_logs("Error encountered while updating data in the database: %s" % (str(err)), status='CRITICAL')
                    raise ValueError("Error encountered while updating data in the database: %s" % (err))  
            finally:
                db_conn.close() 
            
    def jinja_select_query(self, template= None, data=None):
        resultset = []
        query, bind_params = self.jinja.prepare_query(template, data)
        no_except = True
        while no_except:
            try:
                db_conn = self.get_connection()
                cursor = db_conn.cursor(as_dict=True)
                cursor.execute(query,dict(bind_params))
                resultset = cursor.fetchall()
                no_except = False
                cursor.close()
                return resultset
            except Exception as err:
                db_conn.rollback()
                if self.deadlock_validator(err):
                    self.db_logs("Encountered a deadlock on jinja select query", status='CRITICAL')
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                    self.db_logs("Sleeping for 3 seconds...", status='WARNING')
                else:
                    self.db_logs("Error encountered while selecting data from the database: %s" % (str(err)), status='CRITICAL')
                    raise ValueError("Error encountered while selecting data from the database: %s" % (err))  
            finally:   
                db_conn.close()


    def jinja_update_query(self, template= None, data=None):
        query, bind_params = self.jinja.prepare_query(template, data)
        no_except = True
        while no_except:
            try:
                db_conn = self.get_connection()
                cursor = db_conn.cursor()
                cursor.execute(query)
                cursor.close()
                db_conn.commit()
                no_except = False    
            except Exception as err:
                db_conn.rollback()
                if self.deadlock_validator(err):
                    self.db_logs("Encountered a deadlock on jinja update query", status='CRITICAL')
                    cursor.close()
                    db_conn.close()
                    time.sleep(3)
                    self.db_logs("Sleeping for 3 seconds...", status='WARNING')
                else:
                    self.db_logs("Error encountered while updating data in the database: %s" % (str(err)), status='CRITICAL')
                    raise ValueError("Error encountered while updating data in the database: %s" % (err)) 
            finally:
                db_conn.close()

            
    def call_proc(self, query_string=None, params=None):
        db_conn = self.get_connection()
        resultset = []
        try:
            cursor = db_conn.cursor()
            cursor.execute(query_string)
            resultset = cursor.fetchall()
            cursor.close()
            return resultset
        except Exception as err:
            self.db_logs("Error connecting to stored procedure: %s" % (str(err)), status='CRITICAL')
            raise ValueError("Error connecting to stored procedure.")
        finally:
            db_conn.commit()
            db_conn.close()
    
    def truncate_table(self, query_string=None):
        db_conn = self.get_connection()
        try:
            cursor = db_conn.cursor()
            cursor.execute(query_string)
            cursor.close()
        except Exception as err:
            db_conn.rollback()
            self.db_logs("Error encountered while deleting to database: %s" % (str(err)), status='CRITICAL')
            raise ValueError("Error encountered while deleting to database: %s" % (err))
        finally:
            db_conn.commit()
            db_conn.close()
