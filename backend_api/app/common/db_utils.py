from backend_api.app.api import db
from sqlalchemy import exc
from backend_api.app import logger
from backend_api.app.models.error_schema import ErrorObject


class DatabaseUtils():

    list_of_ids = []
    update_commit = db.session


    def __init__(self, *args, **kwargs):
        pass

    def get_all_model_name(self):
        table_names = list()
        for model in db.Model._decl_class_registry.values():
            try:
                table_names.append(model.__tablename__)
            except:
                pass
        return table_names

    def model_session(self, Model):
        return db.session.query(Model)

    def filter_with_paginate(self, model_session, Model,id=None, args=None, params=None):
        try:
            data_query = model_session
            if id is not None:
                data_query = data_query.filter(Model.id==id)
            elif args['start'] != 1 or args['limit'] != 0:
                data_query = data_query.order_by(Model.id.desc()).paginate(args['start'],args['limit'], False).items
            elif params:
                data_query = data_query.filter_by(**params).all()
            else:
                data_query = data_query.order_by(Model.id.desc()).all()
        except Exception as error:
            raise ValueError(ErrorObject(type="PaginateError", message="Error on filter and paginate").to_json())
        finally:
            db.session.close()
            db.engine.dispose()
            return data_query


    def insert_data(self ,module_name, Model, data, commit=False):
        try:
            model = Model(**data)
            db.session.add(model)
            db.session.flush()
            if commit:
                db.session.commit()
            
            return model.id
        except exc.IntegrityError as integrity_err:
            logger.log("Encountered Integrity error while inserting the data : %s" % (integrity_err), log_type='ERROR')
            db.session.rollback()
            raise ValueError(ErrorObject(type="DuplicateEntryError", message="%s already exists." % (module_name)).to_json())
        except exc.DataError as data_err:
            logger.log("Encountered Data error while inserting the data : %s" % (data_err), log_type='ERROR')
            db.session.rollback()
            raise ValueError(ErrorObject(type="MaxLengthError", message="Encountered max length").to_json())
        except Exception as err:
            logger.log("Encountered error while inserting the data : %s" % (err), log_type='ERROR')
            db.session.rollback()
            raise ValueError(ErrorObject(type="InsertError", message="Encountered while inserting the data").to_json())
        finally:
            db.session.close()
            db.engine.dispose()


    def update_data(self, Model, filter_data, data, commit=False):
        try:
            valid_query = Model.query.filter_by(**filter_data).all()
            if valid_query:
                db.session.query(Model).filter_by(**filter_data).update(data)
                db.session.flush()

                if commit:
                    db.session.commit()
                    db.session.close()
                    db.engine.dispose()
                return True
            else:
                return False
        except exc.IntegrityError as integrity_err:

            logger.log("Encountered Integrity error while inserting the data : %s" % (integrity_err), log_type='ERROR')
            raise ValueError(ErrorObject(type="DuplicateEntryError", message="Encountered duplicate data").to_json())
        except exc.DataError as data_err:
            logger.log("Encountered Data error while inserting the data : %s" % (data_err), log_type='ERROR')
            db.session.rollback()
            raise ValueError(ErrorObject(type="MaxLengthError", message="Encountered max length").to_json())
        except ValueError as value_err:
            logger.log("Encountered value error while inserting the data : %s" % (value_err), log_type='ERROR')
            db.session.rollback()
            raise ValueError(ErrorObject(type="ValueError", message=str(value_err)).to_json())

    def select_with_filter(self, Model, Schema, filter):
        _model = Model
        _model_list = db.session.query(_model).filter_by(**filter).all()
        _model_result = Schema(many=True).dump(_model_list)
        db.session.close()
        db.engine.dispose()
        return _model_result

    def select_query_with_filter(self, Model, filter):
        try:
            _model = Model

            _model_list = db.session.query(_model).filter_by(**filter).all()
            db.session.close()
            db.engine.dispose()
            return _model_list
        except Exception as err:
            raise ValueError(ErrorObject(type="QueryError", message="Invalid {table} id : {filter}".format(table=_model().__class__.__name__, filter=filter)).to_json())


    def delete_data_using_id(self, Model, id):
        try:
            valid_query = db.session.query(Model).filter_by(**id).all()
            if valid_query:
                db.session.query(Model).filter_by(**id).delete(synchronize_session=False)
                db.session.commit()
                return True
            else:
                return False
        except Exception as err:
            db.session.rollback()
            logger.log("Encountered value error while deleting the data : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="ExceptionError", 
                message="Encountered error while deleting the data").to_json())
        finally:
            db.session.close()
            db.engine.dispose()

    def model_join(self, Model, Join_Model, *entities):
        try:
            _model_column = Model.__table__.columns
            _model = Model.query.with_entities(*_model_column, *entities).outerjoin(Join_Model)
        except Exception as err:
            raise ValueError(ErrorObject(type="JoinError", message="Error on join tables").to_json())
        finally:
            db.session.close()
            db.engine.dispose()
            return _model


    def model_join_many(self, Model, model, *entities):
        try:
            _model_column = Model.__table__.columns
            _model = Model.query.with_entities(*_model_column, *entities).outerjoin(*model)
            return _model
        except Exception as err:
            raise ValueError(ErrorObject(type="JoinError", message="Error on join tables").to_json())
        finally:
            db.session.close()
            db.engine.dispose()

    def data_rollback(self, list_of_ids):
        for table, ids in list_of_ids.items():
            if ids is not None:
                sql = 'DELETE FROM %s WHERE id = %s' % (table, ids)
                self.execute_raw_query(sql)
        return True

    def single_data_rollback(self, list_of_ids, table_name=None):
        for ids in list_of_ids:
            sql = 'DELETE FROM %s WHERE id = %s' % (table_name, ids)
            self.execute_raw_query(sql)
        return True

    def check_table_if_not_exist(self, table_name):
        try:
            sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '%s'" % (table_name)
            sql_result = self.execute_raw_query(sql)
            table = [row[0] for row in sql_result]
            if len(table) is 0:
                return True
            else:
                return False
        except Exception as err:
            logger.log("Encountered error while checking the table if not exists : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="TableError", message="Error on checking the table if not exists").to_json())

    # def check_column_if_exist_in_table(self, table_name, column_name):
    #     try:
    #         sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS \
    #             where TABLE_NAME = '%s' and COLUMN_NAME = '%s'" % (table_name, column_name)
    #         sql_result = self.execute_raw_query(sql)
    #         column = [row[0] for row in sql_result]
    #         if len(column) is not 0:
    #             return True
    #         raise ValueError(ErrorObject(type="FieldsError", message="Fields is not exist on Target table").to_json())
    #     except Exception as err:
    #         logger.log("Encountered error : %s" % (err), log_type='ERROR')
    #         raise ValueError(ErrorObject(type="ExceptionError", message="Error while finding the columns on table").to_json())
    
    def check_column_if_exist(self, table_name, column_name):
        try:
            sql = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS \
                where TABLE_NAME = '%s' and COLUMN_NAME = '%s'" % (table_name, column_name)
            sql_result = self.execute_raw_query(sql)
            column = [row[0] for row in sql_result]
            if len(column) is not 0:
                return True
            raise ValueError(ErrorObject(type="FieldsError", message="Fields doesn't exist on Target table").to_json())
        except Exception as err:
            logger.log("Encountered error : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="ExceptionError", message="Error on finding the columns on table").to_json())

    def alter_table(self, table_name, fields, status):
        try:
            mode = ""
            status = status.lower()
            if status == 'add':
                mode = 'ADD {} VARCHAR(255)'.format(fields)
            elif status == 'drop':
                mode = 'DROP COLUMN {}'.format(fields)
            sql = """
                ALTER TABLE {0} {1} 
            """.format(table_name, mode)
            self.execute_raw_query(sql)
            return status

        except Exception as err:
            raise ValueError(ErrorObject(type="AlterTableError", message="Encountered while altering the table").to_json())

    def drop_table(self, *table_name):
        try:
            for table in reversed(table_name):
                sql = "DROP TABLE [{0}]".format(table)
                self.execute_raw_query(sql)
        except Exception as err:
            logger.log("Encountered error : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="ExceptionError", message="Table name doesn't exist").to_json())

    def drop_trigger(self, trigger_name, trigger_list=[]):
        for trigger in trigger_list:
            sql = "DROP TRIGGER IF EXISTS [dbo].[trigger_%s]" % (trigger)
            self.execute_raw_query(sql)
        if trigger_name:
            sql = "DROP TRIGGER IF EXISTS [dbo].[trigger_%s]" % (trigger_name)
            self.execute_raw_query(sql)
            
    def execute_raw_query(self, query):
        try:
            return db.engine.execute(query)
        except Exception as err:
            logger.log("Encountered error : %s" % (err), log_type='ERROR')
            raise ValueError(ErrorObject(type="ExceptionError", message="Error on executing the query").to_json())
        finally:
            db.session.commit()
            db.session.close()
            db.engine.dispose()